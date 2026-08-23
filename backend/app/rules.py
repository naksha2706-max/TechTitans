import re
from typing import List, Dict, Any
from urllib.parse import urlparse

def extract_domain_from_url(url: str) -> str:
    if not url:
        return ""
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        if domain.startswith("www."):
            domain = domain[4:]
        # Remove port if present
        if ":" in domain:
            domain = domain.split(":")[0]
        return domain
    except Exception:
        return ""

def extract_domain_from_email(email: str) -> str:
    if not email or "@" not in email:
        return ""
    try:
        return email.strip().split("@")[-1].lower()
    except Exception:
        return ""

# List of common free email domains
FREE_EMAIL_DOMAINS = {
    "gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "icloud.com",
    "aol.com", "zoho.com", "protonmail.com", "mail.com", "yandex.com",
    "gmx.com", "live.com"
}

def check_payment_requested(text: str) -> bool:
    # Look for terms like registration fee, security deposit, pay rs, pay ₹, etc.
    patterns = [
        r"registration\s+fee",
        r"security\s+deposit",
        r"processing\s+fee",
        r"application\s+fee",
        r"training\s+fee",
        r"refundable\s+deposit",
        r"pay\s+(?:₹|rs\.?)\s*\d+",
        r"deposit\s+(?:₹|rs\.?)\s*\d+",
        r"fee\s+(?:₹|rs\.?)\s*\d+",
        r"pay\s+money",
        r"pay\s+registration",
        r"payment\s+required",
        r"fee\s+required",
    ]
    text_lower = text.lower()
    for p in patterns:
        if re.search(p, text_lower):
            return True
    return False

def check_sensitive_info_request(text: str) -> bool:
    # Look for OTP, PIN, Aadhaar, CVV, Card details
    text_lower = text.lower()
    keywords = [
        "otp", "bank pin", "aadhaar", "adhaar", "cvv", "card details",
        "credit card", "debit card", "pin number"
    ]
    for k in keywords:
        if k in text_lower:
            return True
    return False

def check_suspicious_url(website: str, contact_email: str) -> bool:
    if not website:
        return False
    
    website_lower = website.lower()
    # Check free hosting/suspicious patterns
    free_hosting = [".tk", "weebly.com", "wixsite.com", "blogspot.com", "wordpress.com", "webflow.io", "github.io"]
    for pattern in free_hosting:
        if pattern in website_lower:
            return True
            
    # If custom email domain is present, compare domains
    if contact_email:
        web_domain = extract_domain_from_url(website)
        email_domain = extract_domain_from_email(contact_email)
        
        # Skip match check if the email is a consumer domain (handled by another rule)
        if email_domain in FREE_EMAIL_DOMAINS:
            return False
            
        if web_domain and email_domain and web_domain != email_domain:
            return True
            
    return False

def check_unrealistic_salary(salary: str) -> bool:
    if not salary:
        return False
    # Clean the string from commas, currency symbols
    cleaned_salary = re.sub(r'[^\d]', '', salary)
    if not cleaned_salary:
        return False
    try:
        val = int(cleaned_salary)
        # Threshold: > ₹1,00,000 per month
        if val > 100000:
            return True
    except ValueError:
        pass
    return False

def check_urgent_language(text: str) -> bool:
    # Look for urgency triggers
    text_lower = text.lower()
    phrases = [
        "pay within", "limited seats", "immediately", "act now",
        "apply now", "urgent", "immediate", "within 24 hours", "expires soon"
    ]
    for p in phrases:
        if p in text_lower:
            return True
    return False

def check_personal_email_domain(contact_email: str, company_name: str) -> bool:
    if not contact_email or not company_name or not company_name.strip():
        return False
    email_domain = extract_domain_from_email(contact_email)
    return email_domain in FREE_EMAIL_DOMAINS

def check_no_company_info(company_name: str, website: str) -> bool:
    return not company_name or not company_name.strip() or not website or not website.strip()

def evaluate_opportunity(
    company_name: str = "",
    message_text: str = "",
    salary: str = "",
    website: str = "",
    contact_email: str = "",
    prior_report_count: int = 0
) -> Dict[str, Any]:
    warnings = []
    score = 0

    # 1. PAYMENT_REQUESTED (+30)
    if check_payment_requested(message_text):
        warnings.append({
            "code": "PAYMENT_REQUESTED",
            "label": "Registration fee requested",
            "points": 30
        })
        score += 30

    # 2. SENSITIVE_INFO_REQUEST (+20)
    if check_sensitive_info_request(message_text):
        warnings.append({
            "code": "SENSITIVE_INFO_REQUEST",
            "label": "Sensitive info requested",
            "points": 20
        })
        score += 20

    # 3. SUSPICIOUS_URL (+20)
    if check_suspicious_url(website, contact_email):
        warnings.append({
            "code": "SUSPICIOUS_URL",
            "label": "Suspicious website URL",
            "points": 20
        })
        score += 20

    # 4. UNREALISTIC_SALARY (+15)
    if check_unrealistic_salary(salary):
        warnings.append({
            "code": "UNREALISTIC_SALARY",
            "label": "Unrealistically high salary",
            "points": 15
        })
        score += 15

    # 5. URGENT_LANGUAGE (+10)
    if check_urgent_language(message_text):
        warnings.append({
            "code": "URGENT_LANGUAGE",
            "label": "Urgent payment language detected",
            "points": 10
        })
        score += 10

    # 6. PERSONAL_EMAIL_DOMAIN (+10)
    if check_personal_email_domain(contact_email, company_name):
        warnings.append({
            "code": "PERSONAL_EMAIL_DOMAIN",
            "label": "Personal email domain for company",
            "points": 10
        })
        score += 10

    # 7. NO_COMPANY_INFO (+10)
    if check_no_company_info(company_name, website):
        warnings.append({
            "code": "NO_COMPANY_INFO",
            "label": "Missing company information",
            "points": 10
        })
        score += 10

    # 8. PRIOR_REPORTS (+20) - Layered additive signal
    if prior_report_count >= 1:
        warnings.append({
            "code": "PRIOR_REPORTS",
            "label": f"{prior_report_count} other student{'s' if prior_report_count > 1 else ''} reported this contact",
            "points": 20
        })
        score += 20

    # 9. INVALID_SSL (+15) - Phase 5 Domain Intelligence
    if website:
        from app.domain_intel import analyze_domain
        d_intel = analyze_domain(website)
        if d_intel.get("has_ssl_error"):
            warnings.append({
                "code": "INVALID_SSL",
                "label": "Invalid or missing SSL security certificate on company website",
                "points": 15
            })
            score += 15

    # Cap score at 100
    risk_score = min(score, 100)

    # Scoring & Banding
    if risk_score <= 30:
        risk_band = "low"
        recommendation = "This opportunity appears relatively low-risk, but verify the company independently before proceeding."
    elif risk_score <= 60:
        risk_band = "medium"
        recommendation = "Some details couldn't be verified. Confirm the recruiter and company through an independent channel before applying or sharing information."
    else:
        risk_band = "high"
        recommendation = "Multiple high-risk signals were found. Do not pay money or share personal/financial information until this opportunity is independently verified."

    return {
        "risk_score": risk_score,
        "risk_band": risk_band,
        "warnings": warnings,
        "recommendation": recommendation
    }

