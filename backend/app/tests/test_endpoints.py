import os
# Set testing environment variable to bypass rate limits
os.environ["TESTING"] = "True"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.pool import StaticPool
from app.database import Base, get_db
from app.main import app
from app import models

# In-memory SQLite database with StaticPool to keep it alive across sessions
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(name="db")
def session_fixture():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(name="client")
def client_fixture(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

def test_auth_register_and_login(client):
    # Register
    res = client.post("/api/auth/register", json={"email": "student@college.edu", "password": "securepassword"})
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    # Register duplicate email
    res_dup = client.post("/api/auth/register", json={"email": "student@college.edu", "password": "differentpwd"})
    assert res_dup.status_code == 400

    # Login success
    res_login = client.post("/api/auth/login", json={"email": "student@college.edu", "password": "securepassword"})
    assert res_login.status_code == 200
    assert "access_token" in res_login.json()

    # Login fail
    res_fail = client.post("/api/auth/login", json={"email": "student@college.edu", "password": "wrongpassword"})
    assert res_fail.status_code == 400

def test_analyze_opportunity_anonymous(client):
    payload = {
        "company_name": "Unknown Corp",
        "message_text": "Apply to get an internship. No fees required.",
        "salary": "15000",
        "website": "https://unknowncorp.com",
        "contact_email": "hr@unknowncorp.com"
    }
    res = client.post("/api/analyze", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["risk_score"] <= 30
    assert data["risk_band"] == "low"
    assert len(data["warnings"]) == 0

def test_submit_report_and_reputation_lookup(client):
    # Submit report
    report_payload = {
        "company_name": "Scammer Ltd",
        "description": "Demanded ₹3,000 for registration before interview.",
        "contact_email": "hr@scammerltd.com",
        "contact_phone": "+91 99999 88888"
    }
    res = client.post("/api/reports", json=report_payload)
    assert res.status_code == 201
    assert "id" in res.json()
    assert res.json()["status"] == "pending"

    # Submit second report with same email to test count increment
    report_payload2 = {
        "company_name": "Scammer Ltd Duplicate",
        "description": "They asked for processing fee.",
        "contact_email": "hr@scammerltd.com"
    }
    client.post("/api/reports", json=report_payload2)

    # Lookup reputation
    rep_res = client.get("/api/reputation?type=email&value=hr@scammerltd.com")
    assert rep_res.status_code == 200
    assert rep_res.json()["report_count"] == 2
    assert rep_res.json()["risk_level"] == "high"

    # Prior reports triggers additive signal on analyze
    analyze_payload = {
        "company_name": "Scammer Ltd",
        "message_text": "Clean opportunity text here.",
        "contact_email": "hr@scammerltd.com"
    }
    analyze_res = client.post("/api/analyze", json=analyze_payload)
    assert analyze_res.status_code == 200
    data = analyze_res.json()
    # Triggered PRIOR_REPORTS warning (+20 points)
    assert any(w["code"] == "PRIOR_REPORTS" for w in data["warnings"])
    assert data["risk_score"] >= 20

def test_check_history_and_auth_guard(client):
    # History requires auth
    res_no_auth = client.get("/api/checks")
    assert res_no_auth.status_code == 401

    # Register & Login
    client.post("/api/auth/register", json={"email": "user@college.edu", "password": "securepassword"})
    token = client.post("/api/auth/login", json={"email": "user@college.edu", "password": "securepassword"}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Run check as logged in user
    payload = {
        "company_name": "History Corp",
        "message_text": "Standard recruitment text.",
        "salary": "25000",
        "website": "https://historycorp.com",
        "contact_email": "recruitment@historycorp.com"
    }
    res_analyze = client.post("/api/analyze", json=payload, headers=headers)
    assert res_analyze.status_code == 200

    # Get check history
    res_history = client.get("/api/checks", headers=headers)
    assert res_history.status_code == 200
    checks = res_history.json()["checks"]
    assert len(checks) == 1
    assert checks[0]["company_name"] == "History Corp"

def test_empty_contact_hashing_prevention(client):
    # Submit report with empty/whitespace contact details
    report_payload = {
        "company_name": "Ghost Ltd",
        "description": "Asked for money",
        "contact_email": "   ",
        "contact_phone": "",
        "contact_upi": " "
    }
    res = client.post("/api/reports", json=report_payload)
    assert res.status_code == 201

    # Verify that lookup for empty/whitespace email/phone/upi returns 0 reports
    res_email = client.get("/api/reputation?type=email&value=")
    assert res_email.status_code == 200
    assert res_email.json()["report_count"] == 0

    res_phone = client.get("/api/reputation?type=phone&value= ")
    assert res_phone.status_code == 200
    assert res_phone.json()["report_count"] == 0

    res_upi = client.get("/api/reputation?type=upi&value=   ")
    assert res_upi.status_code == 200
    assert res_upi.json()["report_count"] == 0

    # Also verify that analyzing with empty contact email doesn't trigger PRIOR_REPORTS
    analyze_payload = {
        "company_name": "Ghost Ltd",
        "message_text": "Check opportunity",
        "contact_email": "   "
    }
    res_analyze = client.post("/api/analyze", json=analyze_payload)
    assert res_analyze.status_code == 200
    data = res_analyze.json()
    assert not any(w["code"] == "PRIOR_REPORTS" for w in data["warnings"])

