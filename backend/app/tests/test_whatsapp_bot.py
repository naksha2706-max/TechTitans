from app.whatsapp_bot import process_whatsapp_message

def test_process_whatsapp_text():
    res = process_whatsapp_message(
        sender="+919876543210",
        message_text="You got selected for internship! Pay ₹1,500 registration fee immediately."
    )
    assert "ScamCheck WhatsApp Bot" in res["reply"]
    assert "HIGH" in res["reply"] or "MEDIUM" in res["reply"]

def test_process_whatsapp_upi():
    res = process_whatsapp_message(
        sender="+919876543210",
        message_text="Pay to upi refund-hr@ybl enter PIN to receive money"
    )
    assert "UPI Scam Analysis" in res["reply"]
