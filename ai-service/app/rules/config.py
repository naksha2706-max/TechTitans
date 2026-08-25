"""
Signal catalogue for the risk engine (see docs/FEATURE_SPECIFICATION.md).
Update this file in the same commit as that doc — they must never drift
apart (AGENTS.md rule 6 applies to this spec too, even though it's not a
DB schema).

Each entry in SIGNAL_CATALOGUE is metadata only (weight + human-readable
label). The actual detection logic lives in scorer.py as Signal subclasses;
this module never imports from scorer.py to avoid a circular dependency.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class SignalSpec:
    code: str
    weight: int
    label: str


SIGNAL_CATALOGUE: tuple[SignalSpec, ...] = (
    SignalSpec("PAYMENT_REQUESTED", 30, "Message requests an upfront payment or fee"),
    SignalSpec("SENSITIVE_INFO_REQUEST", 20, "Message asks for OTP, bank PIN, Aadhaar, or card details"),
    SignalSpec("SUSPICIOUS_URL", 20, "Website domain doesn't match contact email domain, or uses a free-hosting pattern"),
    SignalSpec("UNREALISTIC_SALARY", 15, "Stated salary is implausible for an unspecified/entry-level role"),
    SignalSpec("URGENT_LANGUAGE", 10, "Message uses urgency phrases like 'act now' or 'limited seats'"),
    SignalSpec("PERSONAL_EMAIL_DOMAIN", 10, "Contact email uses a free consumer domain while claiming to represent a company"),
    SignalSpec("NO_COMPANY_INFO", 10, "Company name or website is missing"),
    SignalSpec("PRIOR_REPORTS", 20, "N other students reported this contact"),  # applied separately, additive
)

# Ordered ascending by upper bound so scorer.py can walk it with a simple
# "first bound the score fits under" scan instead of a keyed dict lookup.
BAND_LADDER: tuple[tuple[int, str], ...] = (
    (30, "low"),
    (60, "medium"),
    (100, "high"),
)

RECOMMENDATION_TEXT = {
    "low": "This opportunity appears relatively low-risk, but verify the company independently before proceeding.",
    "medium": "Some details couldn't be verified. Confirm the recruiter and company through an independent channel before applying or sharing information.",
    "high": "Multiple high-risk signals were found. Do not pay money or share personal/financial information until this opportunity is independently verified.",
}

FREE_EMAIL_DOMAINS = frozenset({"gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "rediffmail.com"})
FREE_HOSTING_PATTERNS = ("weebly", "wixsite", ".tk", ".ml", ".ga")

MAX_SCORE = 100


def band_for_score(score: int) -> str:
    for upper_bound, band in BAND_LADDER:
        if score <= upper_bound:
            return band
    return "high"


def spec_for(code: str) -> SignalSpec:
    for spec in SIGNAL_CATALOGUE:
        if spec.code == code:
            return spec
    raise KeyError(f"Unknown signal code: {code}")
