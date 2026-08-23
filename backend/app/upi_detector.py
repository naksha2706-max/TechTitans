import re
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app import normalizers, models

# Common scam patterns in fake recruiter / refund UPI handles
SUSPICIOUS_HANDLE_KEYWORDS = [
    "refund", "helpdesk", "customercare", "customer-care", "support",
    "hr-deposit", "job-fee", "registration", "verification", "recruitment-fee",
    "payment-gateway", "security-deposit"
]

# Patterns for UPI PIN scam / Collect request fraud
PIN_FRAUD_PATTERNS = [
    r"enter\s+(?:upi\s+)?pin\s+to\s+receive",
    r"enter\s+(?:upi\s+)?pin\s+to\s+get",
    r"enter\s+(?:upi\s+)?pin\s+to\s+credit",
    r"enter\s+(?:upi\s+)?pin\s+to\s+claim",
    r"enter\s+(?:upi\s+)?pin\s+for\s+(?:refund|cashback|salary|stipend)",
    r"pay\s+rs\.?\s*\d+\s+to\s+receive",
    r"collect\s+request",
    r"accept\s+request\s+to\s+receive",
    r"pin\s+required\s+for\s+credit"
]

def analyze_upi_transaction(
    upi_id: str = "",
    message_text: str = "",
    amount: str = "",
    db: Session = None
) -> Dict[str, Any]:
    warnings: List[Dict[str, Any]] = []
    score = 0

    norm_upi = normalizers.normalize_upi(upi_id) if upi_id else ""
    msg_lower = (message_text or "").lower()

    # Rule 1: UPI PIN Fraud / Fake Collect Request (+40 pts)
    for pattern in PIN_FRAUD_PATTERNS:
        if re.search(pattern, msg_lower):
            warnings.append({
                "code": "UPI_PIN_FRAUD",
                "label": "Fake receive money trap detected! Entering a UPI PIN ALWAYS deducts money from your account, never credits it.",
                "points": 40
            })
            score += 40
            break

    # Rule 2: Suspicious UPI Handle Keywords (+20 pts)
    if norm_upi:
        handle_prefix = norm_upi.split("@")[0] if "@" in norm_upi else norm_upi
        for kw in SUSPICIOUS_HANDLE_KEYWORDS:
            if kw in handle_prefix:
                warnings.append({
                    "code": "SUSPICIOUS_UPI_HANDLE",
                    "label": f"UPI handle contains suspicious recruiter/refund keyword '{kw}'",
                    "points": 20
                })
                score += 20
                break

    # Rule 3: Database Reputation Lookup (+30 pts)
    if norm_upi and db:
        upi_hash = normalizers.hash_contact(norm_upi)
        rep = db.query(models.ContactReputation).filter(
            models.ContactReputation.contact_hash == upi_hash
        ).first()
        
        if rep and rep.report_count >= 1:
            warnings.append({
                "code": "PRIOR_UPI_REPORTS",
                "label": f"This UPI handle has been reported by {rep.report_count} other student{'s' if rep.report_count > 1 else ''} as fraudulent",
                "points": 30
            })
            score += 30

    # Rule 4: Payment Requested for Onboarding (+20 pts)
    if any(k in msg_lower for k in ["registration", "deposit", "fee", "processing", "pay rs", "pay ₹"]):
        if not any(w["code"] == "UPI_PIN_FRAUD" for w in warnings):
            warnings.append({
                "code": "UPI_PAYMENT_DEMAND",
                "label": "Payment requested for job/internship onboarding",
                "points": 20
            })
            score += 20

    risk_score = min(score, 100)

    if risk_score <= 20:
        risk_band = "low"
        recommendation = "No obvious UPI scam triggers detected. Always verify the recruiter's official identity before sending any funds."
    elif risk_score <= 55:
        risk_band = "medium"
        recommendation = "Caution advised. Verify this payment request directly through the company's official corporate portal."
    else:
        risk_band = "high"
        recommendation = "HIGH RISK SCAM WARNING: Do not enter your UPI PIN or send money. Legitimate companies never charge students to work or receive stipend."

    return {
        "upi_id": norm_upi,
        "risk_score": risk_score,
        "risk_band": risk_band,
        "warnings": warnings,
        "recommendation": recommendation
    }
