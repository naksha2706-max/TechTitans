"""
Matches docs/FEATURE_SPECIFICATION.md exactly. If that doc changes, update
this file in the same commit — they must never drift apart (AGENTS.md rule 6
applies to this spec too, even though it's not a DB schema).
"""

# code -> (points, label shown in the warnings array)
RULES = {
    "PAYMENT_REQUESTED": (30, "Message requests an upfront payment or fee"),
    "SENSITIVE_INFO_REQUEST": (20, "Message asks for OTP, bank PIN, Aadhaar, or card details"),
    "SUSPICIOUS_URL": (20, "Website domain doesn't match contact email domain, or uses a free-hosting pattern"),
    "UNREALISTIC_SALARY": (15, "Stated salary is implausible for an unspecified/entry-level role"),
    "URGENT_LANGUAGE": (10, "Message uses urgency phrases like 'act now' or 'limited seats'"),
    "PERSONAL_EMAIL_DOMAIN": (10, "Contact email uses a free consumer domain while claiming to represent a company"),
    "NO_COMPANY_INFO": (10, "Company name or website is missing"),
    "PRIOR_REPORTS": (20, "N other students reported this contact"),  # applied separately, additive
}

BAND_THRESHOLDS = {
    "low": (0, 30),
    "medium": (31, 60),
    "high": (61, 100),
}

RECOMMENDATION_TEXT = {
    "low": "This opportunity appears relatively low-risk, but verify the company independently before proceeding.",
    "medium": "Some details couldn't be verified. Confirm the recruiter and company through an independent channel before applying or sharing information.",
    "high": "Multiple high-risk signals were found. Do not pay money or share personal/financial information until this opportunity is independently verified.",
}

FREE_EMAIL_DOMAINS = {"gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "rediffmail.com"}
FREE_HOSTING_PATTERNS = ("weebly", "wixsite", ".tk", ".ml", ".ga")


def band_for_score(score: int) -> str:
    for band, (low, high) in BAND_THRESHOLDS.items():
        if low <= score <= high:
            return band
    return "high"
