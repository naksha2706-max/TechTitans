from app.upi_detector import analyze_upi_transaction

def test_upi_pin_fraud_detection():
    res = analyze_upi_transaction(
        upi_id="recruiter@okaxis",
        message_text="Enter your UPI PIN to receive ₹5,000 stipend credit"
    )
    assert res["risk_band"] == "high"
    assert any(w["code"] == "UPI_PIN_FRAUD" for w in res["warnings"])

def test_suspicious_upi_handle():
    res = analyze_upi_transaction(
        upi_id="job-refund-helpdesk@ybl",
        message_text="Send 500 for processing"
    )
    assert any(w["code"] == "SUSPICIOUS_UPI_HANDLE" for w in res["warnings"])

def test_clean_upi_id():
    res = analyze_upi_transaction(
        upi_id="john.doe@okicici",
        message_text="Valid inquiry"
    )
    assert res["risk_band"] == "low"
