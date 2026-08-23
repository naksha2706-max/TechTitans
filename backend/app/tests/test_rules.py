from app.rules import (
    check_payment_requested,
    check_sensitive_info_request,
    check_suspicious_url,
    check_unrealistic_salary,
    check_urgent_language,
    check_personal_email_domain,
    check_no_company_info,
    evaluate_opportunity
)

def test_payment_requested():
    assert check_payment_requested("Pay ₹2,000 registration fee to confirm your seat") is True
    assert check_payment_requested("Please pay a refundable security deposit of Rs 3000") is True
    assert check_payment_requested("No fees required to apply for this job") is False

def test_sensitive_info_request():
    assert check_sensitive_info_request("Share your Aadhaar number and OTP to proceed") is True
    assert check_sensitive_info_request("Provide bank pin and card details") is True
    assert check_sensitive_info_request("Please attach your resume and cover letter") is False

def test_suspicious_url():
    # website domain != contact email domain
    assert check_suspicious_url("http://scam-site.tk", "hr@company.com") is True
    # uses free hosting pattern
    assert check_suspicious_url("https://company.weebly.com", "hr@company.weebly.com") is True
    # both match correctly
    assert check_suspicious_url("https://company.com", "hr@company.com") is False
    # email is a consumer domain (should not trigger mismatch warning)
    assert check_suspicious_url("https://company.com", "hr@gmail.com") is False

def test_unrealistic_salary():
    assert check_unrealistic_salary("200000") is True
    assert check_unrealistic_salary("₹150,000 per month") is True
    assert check_unrealistic_salary("15000") is False
    assert check_unrealistic_salary("Competitive salary") is False

def test_urgent_language():
    assert check_urgent_language("Pay within 1 hour or lose your seat") is True
    assert check_urgent_language("Apply immediately for immediate consideration") is True
    assert check_urgent_language("Please apply by Friday if possible") is False

def test_personal_email_domain():
    assert check_personal_email_domain("hr@gmail.com", "ABC Technologies") is True
    assert check_personal_email_domain("hr@company.com", "ABC Technologies") is False
    assert check_personal_email_domain("hr@gmail.com", "") is False

def test_no_company_info():
    assert check_no_company_info("", "https://company.com") is True
    assert check_no_company_info("ABC", "") is True
    assert check_no_company_info("ABC", "https://company.com") is False

def test_evaluate_opportunity():
    # High risk evaluation
    res_high = evaluate_opportunity(
        company_name="Fake Co",
        message_text="Pay ₹2,000 registration fee immediately. OTP required.",
        salary="250000",
        website="https://fakeco.tk",
        contact_email="hr@gmail.com"
    )
    assert res_high["risk_score"] >= 61
    assert res_high["risk_band"] == "high"
    assert any(w["code"] == "PAYMENT_REQUESTED" for w in res_high["warnings"])
    assert any(w["code"] == "SENSITIVE_INFO_REQUEST" for w in res_high["warnings"])

    # Low risk evaluation
    res_low = evaluate_opportunity(
        company_name="Valid Co",
        message_text="We are looking for interns. Apply on our site.",
        salary="15000",
        website="https://validco.com",
        contact_email="hr@validco.com"
    )
    assert res_low["risk_score"] <= 30
    assert res_low["risk_band"] == "low"
    assert len(res_low["warnings"]) == 0
