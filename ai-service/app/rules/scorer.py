"""
Risk engine for POST /analyze.

Architecture: each detector is a small `Signal` object that knows how to
inspect an `AnalyzeContext` and decide whether it fires. `RiskEngine` just
runs the registered signals, sums their weights (capped at MAX_SCORE), and
maps the total onto a band. This keeps each detection rule isolated and
independently testable, and makes adding/removing a signal a matter of
editing the registry tuple rather than a chain of if-statements.

Pure — no DB/network calls in here. The backend looks up
`reputation_hit_count` (contact_reputation table) and passes it in via
AnalyzeContext, same for any other pre-computed inputs.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from .config import (
    FREE_EMAIL_DOMAINS,
    FREE_HOSTING_PATTERNS,
    MAX_SCORE,
    RECOMMENDATION_TEXT,
    band_for_score,
    spec_for,
)

_PAYMENT_RE = re.compile(
    r"(registration fee|security deposit|processing fee|caution money|pay\s*(₹|rs\.?|inr)\s*\d+)",
    re.IGNORECASE,
)
_SENSITIVE_INFO_RE = re.compile(
    r"\b(otp|bank pin|aadhaar|aadhar|card number|cvv|card details)\b", re.IGNORECASE
)
_URGENCY_RE = re.compile(
    r"(pay within \d+ hour|limited seats?|immediately|act now|hurry)", re.IGNORECASE
)


def _extract_domain(value: str) -> str:
    if "@" in value:
        return value.rsplit("@", 1)[-1].lower().strip()
    return re.sub(r"^https?://", "", value).split("/", 1)[0].lower().strip()


@dataclass
class AnalyzeContext:
    """Everything a signal might need, bundled once per request."""

    message_text: str
    company_name: str | None = None
    salary: str | None = None
    website: str | None = None
    contact_email: str | None = None
    reputation_hit_count: int = 0


@dataclass
class Verdict:
    """What a single Signal decided when checked against a context."""

    fired: bool
    label_override: str | None = None


class Signal:
    """Base class for a single detection rule. Subclasses implement check()."""

    code: str = ""

    def check(self, ctx: AnalyzeContext) -> Verdict:
        raise NotImplementedError

    def evaluate(self, ctx: AnalyzeContext) -> Verdict:
        return self.check(ctx)


class PaymentRequestSignal(Signal):
    code = "PAYMENT_REQUESTED"

    def check(self, ctx: AnalyzeContext) -> Verdict:
        return Verdict(fired=bool(_PAYMENT_RE.search(ctx.message_text)))


class SensitiveInfoSignal(Signal):
    code = "SENSITIVE_INFO_REQUEST"

    def check(self, ctx: AnalyzeContext) -> Verdict:
        return Verdict(fired=bool(_SENSITIVE_INFO_RE.search(ctx.message_text)))


class SuspiciousUrlSignal(Signal):
    code = "SUSPICIOUS_URL"

    def check(self, ctx: AnalyzeContext) -> Verdict:
        if not ctx.website:
            return Verdict(fired=False)
        website_domain = _extract_domain(ctx.website)
        email_domain = _extract_domain(ctx.contact_email) if ctx.contact_email else None
        looks_free_hosted = any(pattern in website_domain for pattern in FREE_HOSTING_PATTERNS)
        domain_mismatch = email_domain is not None and email_domain != website_domain
        return Verdict(fired=looks_free_hosted or domain_mismatch)


class UnrealisticSalarySignal(Signal):
    code = "UNREALISTIC_SALARY"

    def check(self, ctx: AnalyzeContext) -> Verdict:
        if not ctx.salary:
            return Verdict(fired=False)
        digits = re.sub(r"[^\d]", "", ctx.salary)
        fired = bool(digits) and int(digits) > 100_000
        return Verdict(fired=fired)


class UrgentLanguageSignal(Signal):
    code = "URGENT_LANGUAGE"

    def check(self, ctx: AnalyzeContext) -> Verdict:
        return Verdict(fired=bool(_URGENCY_RE.search(ctx.message_text)))


class PersonalEmailDomainSignal(Signal):
    code = "PERSONAL_EMAIL_DOMAIN"

    def check(self, ctx: AnalyzeContext) -> Verdict:
        if not ctx.contact_email:
            return Verdict(fired=False)
        return Verdict(fired=_extract_domain(ctx.contact_email) in FREE_EMAIL_DOMAINS)


class MissingCompanyInfoSignal(Signal):
    code = "NO_COMPANY_INFO"

    def check(self, ctx: AnalyzeContext) -> Verdict:
        no_company = not ctx.company_name or not ctx.company_name.strip()
        no_website = not ctx.website or not ctx.website.strip()
        return Verdict(fired=no_company or no_website)


class PriorReportsSignal(Signal):
    code = "PRIOR_REPORTS"

    def check(self, ctx: AnalyzeContext) -> Verdict:
        if ctx.reputation_hit_count < 1:
            return Verdict(fired=False)
        return Verdict(
            fired=True,
            label_override=f"{ctx.reputation_hit_count} other students reported this contact",
        )


# Registry of active signals. Order only affects the order warnings appear
# in the response, not the total score.
DEFAULT_SIGNALS: tuple[Signal, ...] = (
    PaymentRequestSignal(),
    SensitiveInfoSignal(),
    SuspiciousUrlSignal(),
    UnrealisticSalarySignal(),
    UrgentLanguageSignal(),
    PersonalEmailDomainSignal(),
    MissingCompanyInfoSignal(),
    PriorReportsSignal(),
)


@dataclass
class AnalyzeResult:
    risk_score: int
    risk_band: str
    warnings: list = field(default_factory=list)
    recommendation: str = ""

    def to_dict(self) -> dict:
        return {
            "risk_score": self.risk_score,
            "risk_band": self.risk_band,
            "warnings": self.warnings,
            "recommendation": self.recommendation,
        }


class RiskEngine:
    """Runs a set of Signals against a context and totals the result."""

    def __init__(self, signals: tuple[Signal, ...] = DEFAULT_SIGNALS):
        self._signals = signals

    def evaluate(self, ctx: AnalyzeContext) -> AnalyzeResult:
        total = 0
        warnings = []

        for signal in self._signals:
            verdict = signal.evaluate(ctx)
            if not verdict.fired:
                continue
            spec = spec_for(signal.code)
            total += spec.weight
            warnings.append({
                "code": spec.code,
                "points": spec.weight,
                "label": verdict.label_override or spec.label,
            })

        total = min(total, MAX_SCORE)
        band = band_for_score(total)
        return AnalyzeResult(
            risk_score=total,
            risk_band=band,
            warnings=warnings,
            recommendation=RECOMMENDATION_TEXT[band],
        )


_default_engine = RiskEngine()


def analyze(
    message_text: str,
    *,
    company_name: str | None = None,
    salary: str | None = None,
    website: str | None = None,
    contact_email: str | None = None,
    reputation_hit_count: int = 0,
) -> AnalyzeResult:
    """Thin functional wrapper so callers (and existing tests) don't need
    to know about RiskEngine/AnalyzeContext directly."""
    ctx = AnalyzeContext(
        message_text=message_text,
        company_name=company_name,
        salary=salary,
        website=website,
        contact_email=contact_email,
        reputation_hit_count=reputation_hit_count,
    )
    return _default_engine.evaluate(ctx)
