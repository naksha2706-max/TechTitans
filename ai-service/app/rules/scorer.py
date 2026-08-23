"""
Implements every rule in docs/FEATURE_SPECIFICATION.md for POST /api/analyze.
Pure function — no DB/network calls in here. The backend looks up
`reputation_hit` (contact_reputation table) and passes it in, same for any
other pre-computed inputs. This keeps the module trivial to unit test.
"""

import re
from dataclasses import dataclass, field

from .config import FREE_EMAIL_DOMAINS, FREE_HOSTING_PATTERNS, RULES, band_for_score

PAYMENT_PATTERN = re.compile(
    r"(registration fee|security deposit|processing fee|caution money|pay\s*(₹|rs\.?|inr)\s*\d+)",
    re.IGNORECASE,
)
SENSITIVE_INFO_PATTERN = re.compile(
    r"\b(otp|bank pin|aadhaar|aadhar|card number|cvv|card details)\b", re.IGNORECASE
)
URGENT_PATTERN = re.compile(
    r"(pay within \d+ hour|limited seats?|immediately|act now|hurry)", re.IGNORECASE
)


@dataclass
class AnalyzeResult:
    risk_score: int
    risk_band: str
    warnings: list = field(default_factory=list)
    recommendation: str = ""

    def to_dict(self):
        return {
            "risk_score": self.risk_score,
            "risk_band": self.risk_band,
            "warnings": self.warnings,
            "recommendation": self.recommendation,
        }


def _domain_of(email_or_url: str) -> str:
    if "@" in email_or_url:
        return email_or_url.split("@")[-1].lower().strip()
    return re.sub(r"^https?://", "", email_or_url).split("/")[0].lower().strip()


def analyze(
    message_text: str,
    *,
    company_name: str | None = None,
    salary: str | None = None,
    website: str | None = None,
    contact_email: str | None = None,
    reputation_hit_count: int = 0,
) -> AnalyzeResult:
    from .config import RECOMMENDATION_TEXT  # local import avoids circulars in tests

    score = 0
    warnings = []

    def fire(code: str, label_override: str | None = None):
        nonlocal score
        points, label = RULES[code]
        score += points
        warnings.append({"code": code, "points": points, "label": label_override or label})

    if PAYMENT_PATTERN.search(message_text):
        fire("PAYMENT_REQUESTED")

    if SENSITIVE_INFO_PATTERN.search(message_text):
        fire("SENSITIVE_INFO_REQUEST")

    if website:
        website_domain = _domain_of(website)
        email_domain = _domain_of(contact_email) if contact_email else None
        looks_free_hosted = any(p in website_domain for p in FREE_HOSTING_PATTERNS)
        mismatched = email_domain is not None and email_domain != website_domain
        if looks_free_hosted or mismatched:
            fire("SUSPICIOUS_URL")

    if salary:
        digits = re.sub(r"[^\d]", "", salary)
        if digits and int(digits) > 100000:
            fire("UNREALISTIC_SALARY")

    if URGENT_PATTERN.search(message_text):
        fire("URGENT_LANGUAGE")

    if contact_email:
        if _domain_of(contact_email) in FREE_EMAIL_DOMAINS:
            fire("PERSONAL_EMAIL_DOMAIN")

    if not company_name or not company_name.strip() or not website or not website.strip():
        fire("NO_COMPANY_INFO")

    if reputation_hit_count >= 1:
        fire("PRIOR_REPORTS", label_override=f"{reputation_hit_count} other students reported this contact")

    score = min(score, 100)
    band = band_for_score(score)
    return AnalyzeResult(
        risk_score=score,
        risk_band=band,
        warnings=warnings,
        recommendation=RECOMMENDATION_TEXT[band],
    )
