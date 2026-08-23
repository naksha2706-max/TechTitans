from app.fingerprint_engine import generate_text_fingerprint

def test_generate_text_fingerprint():
    f1 = generate_text_fingerprint("Pay registration fee to HR")
    f2 = generate_text_fingerprint("pay  registration   fee to hr ")
    assert f1 == f2
    assert len(f1) == 64  # SHA-256 hex string length
