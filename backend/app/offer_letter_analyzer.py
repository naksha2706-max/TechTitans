import re
from typing import Dict, Any, List

FREE_EMAIL_DOMAINS = {"gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "icloud.com"}

def analyze_offer_letter(document_text: str = "", filename: str = "") -> Dict[str, Any]:
    """
    Parses offer letter text to identify red flags like security deposit demands,
    free consumer email domain footers, direct selection without interview, and missing CIN details.
    """
    warnings: List[Dict[str, Any]] = []
    score = 0
    text_lower = (document_text or "").lower()

    # Rule 1: OFFER_PAYMENT_CLAUSE (+35 pts)
    payment_terms = [
        "security deposit", "laptop fee", "training fee", "refundable deposit",
        "registration fee", "processing fee", "pay rs", "pay ₹", "equipment fee"
    ]
    for term in payment_terms:
        if term in text_lower:
            warnings.append({
                "code": "OFFER_PAYMENT_CLAUSE",
                "label": f"Offer letter contains payment clause requiring '{term}'. Legitimate companies never demand money before or upon joining.",
                "points": 35
            })
            score += 35
            break

    # Rule 2: UNOFFICIAL_LETTERHEAD_EMAIL (+25 pts)
    for free_domain in FREE_EMAIL_DOMAINS:
        if free_domain in text_lower:
            warnings.append({
                "code": "UNOFFICIAL_LETTERHEAD_EMAIL",
                "label": f"Offer letter uses free consumer email address (@{free_domain}) instead of an official company domain.",
                "points": 25
            })
            score += 25
            break

    # Rule 3: IMMEDIATE_SELECTION_NO_INTERVIEW (+20 pts)
    selection_phrases = [
        "selected without interview", "direct selection", "no interview required",
        "direct hiring", "instant offer letter"
    ]
    for phrase in selection_phrases:
        if phrase in text_lower:
            warnings.append({
                "code": "IMMEDIATE_SELECTION_NO_INTERVIEW",
                "label": "Offer letter claims selection without any formal interview process.",
                "points": 20
            })
            score += 20
            break

    # Rule 4: URGENT_JOINING_PAYMENT (+15 pts)
    if any(k in text_lower for k in ["within 24 hours", "pay immediately", "limited seats available"]):
        warnings.append({
            "code": "URGENT_JOINING_PAYMENT",
            "label": "Urgency clause demanding immediate payment or response within 24 hours.",
            "points": 15
        })
        score += 15

    # Rule 5: MISSING_COMPANY_DETAILS (+15 pts)
    if not re.search(r"\b(?:cin|gstin|reg(?:istration)?\s*no|tax\s*id)\b", text_lower):
        warnings.append({
            "code": "MISSING_COMPANY_DETAILS",
            "label": "No Corporate Identification Number (CIN) or Tax/GST registration details found in letterhead.",
            "points": 15
        })
        score += 15

    risk_score = min(score, 100)

    if risk_score <= 25:
        risk_band = "low"
        recommendation = "The offer letter contains standard employment clauses. Verify HR contact details directly on the company's official website."
    elif risk_score <= 55:
        risk_band = "medium"
        recommendation = "Suspicious formatting or missing corporate info found. Confirm the offer with the company's verified HR department before accepting."
    else:
        risk_band = "high"
        recommendation = "HIGH RISK FAKE OFFER LETTER: Multiple fraudulent indicators detected (payment demand or unofficial contact). Do not transfer any money."

    return {
        "filename": filename or "document_text",
        "risk_score": risk_score,
        "risk_band": risk_band,
        "warnings": warnings,
        "recommendation": recommendation
    }
