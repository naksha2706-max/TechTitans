from app.offer_letter_analyzer import analyze_offer_letter

def test_offer_letter_fake_indicators():
    res = analyze_offer_letter(
        document_text="OFFER LETTER: Selected without interview! Please pay refundable security deposit of Rs 5000. Contact hr@gmail.com within 24 hours.",
        filename="Fake_Offer_Letter.pdf"
    )
    assert res["risk_band"] == "high"
    assert any(w["code"] == "OFFER_PAYMENT_CLAUSE" for w in res["warnings"])
    assert any(w["code"] == "UNOFFICIAL_LETTERHEAD_EMAIL" for w in res["warnings"])

def test_offer_letter_clean():
    res = analyze_offer_letter(
        document_text="Official Employment Offer from Tech Corp. CIN: U12345MH2020PTC123456. Contact hr@techcorp.com",
        filename="Official_Offer.pdf"
    )
    assert res["risk_band"] == "low"
