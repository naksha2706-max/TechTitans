import os
import time
from collections import defaultdict
from typing import Optional, Dict, List

from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app import models, schemas, auth, normalizers, rules
from app.database import engine, Base, get_db

# Initialize database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="ScamCheck API", version="0.1.0")

# Setup CORS middleware to allow connection from the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for dev simplicity
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- In-memory Rate Limiting ---
rate_limit_records = defaultdict(list)

def check_rate_limit(request: Request):
    # Bypass rate limits in testing mode
    if os.environ.get("TESTING") == "True":
        return
        
    ip = request.client.host if request.client else "unknown"
    now = time.time()
    window = 600  # 10 minutes in seconds
    max_requests = 20

    # Clean old requests
    rate_limit_records[ip] = [t for t in rate_limit_records[ip] if now - t < window]

    if len(rate_limit_records[ip]) >= max_requests:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests. Please try again later."
        )
    rate_limit_records[ip].append(now)

# --- Routes ---

@app.post("/api/auth/register", response_model=schemas.TokenResponse)
def register(req: schemas.AuthRequest, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == req.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed_pwd = auth.get_password_hash(req.password)
    user = models.User(email=req.email, password_hash=hashed_pwd)
    db.add(user)
    db.commit()
    db.refresh(user)
    
    token = auth.create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/api/auth/login", response_model=schemas.TokenResponse)
def login(req: schemas.AuthRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == req.email).first()
    if not user or not auth.verify_password(req.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
        
    token = auth.create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/api/analyze", response_model=schemas.AnalyzeResponse)
def analyze_opportunity(
    req: schemas.AnalyzeRequest,
    request: Request,
    db: Session = Depends(get_db),
    user: Optional[models.User] = Depends(auth.get_optional_current_user)
):
    check_rate_limit(request)
    
    prior_report_count = 0
    hashes_to_check = []
    
    if req.contact_email:
        norm_email = normalizers.normalize_email(req.contact_email)
        if norm_email:
            email_hash = normalizers.hash_contact(norm_email)
            hashes_to_check.append(email_hash)
        
    if hashes_to_check:
        reputations = db.query(models.ContactReputation).filter(
            models.ContactReputation.contact_hash.in_(hashes_to_check)
        ).all()
        prior_report_count = sum(r.report_count for r in reputations)
        
    evaluation = rules.evaluate_opportunity(
        company_name=req.company_name or "",
        message_text=req.message_text,
        salary=req.salary or "",
        website=req.website or "",
        contact_email=req.contact_email or "",
        prior_report_count=prior_report_count
    )
    
    # Save check to database
    user_id = user.id if user else None
    check_row = models.Check(
        user_id=user_id,
        company_name=req.company_name,
        message_text=req.message_text,
        salary=req.salary,
        website=req.website,
        contact_email=req.contact_email,
        risk_score=evaluation["risk_score"],
        risk_band=evaluation["risk_band"],
        warnings=evaluation["warnings"]
    )
    db.add(check_row)
    db.commit()
    
    return evaluation

@app.post("/api/reports", status_code=201, response_model=schemas.ReportResponse)
def submit_report(
    req: schemas.ReportRequest,
    request: Request,
    db: Session = Depends(get_db),
    user: Optional[models.User] = Depends(auth.get_optional_current_user)
):
    check_rate_limit(request)
    
    email_hash = None
    phone_hash = None
    upi_hash = None
    contacts_to_upsert = []
    
    if req.contact_email:
        norm_email = normalizers.normalize_email(req.contact_email)
        if norm_email:
            email_hash = normalizers.hash_contact(norm_email)
            contacts_to_upsert.append((email_hash, "email"))
        else:
            email_hash = None
        
    if req.contact_phone:
        norm_phone = normalizers.normalize_phone(req.contact_phone)
        if norm_phone:
            phone_hash = normalizers.hash_contact(norm_phone)
            contacts_to_upsert.append((phone_hash, "phone"))
        else:
            phone_hash = None
        
    if req.contact_upi:
        norm_upi = normalizers.normalize_upi(req.contact_upi)
        if norm_upi:
            upi_hash = normalizers.hash_contact(norm_upi)
            contacts_to_upsert.append((upi_hash, "upi"))
        else:
            upi_hash = None
        
    user_id = user.id if user else None
    report_row = models.ScamReport(
        user_id=user_id,
        company_name=req.company_name,
        description=req.description,
        contact_email_hash=email_hash,
        contact_phone_hash=phone_hash,
        contact_upi_hash=upi_hash,
        status="pending"
    )
    db.add(report_row)
    db.commit()
    db.refresh(report_row)
    
    # Upsert reputation record
    for c_hash, c_type in contacts_to_upsert:
        rep = db.query(models.ContactReputation).filter(
            models.ContactReputation.contact_hash == c_hash
        ).first()
        
        if rep:
            rep.report_count += 1
            rep.last_reported_at = func.now()
        else:
            rep = models.ContactReputation(
                contact_hash=c_hash,
                contact_type=c_type,
                report_count=1,
                last_reported_at=func.now()
            )
            db.add(rep)
            
    db.commit()
    
    return {"id": report_row.id, "status": report_row.status}

@app.get("/api/reputation", response_model=schemas.ReputationResponse)
def lookup_reputation(
    type: str,
    value: str,
    db: Session = Depends(get_db)
):
    if type not in ("email", "phone", "upi"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid contact type"
        )
        
    if type == "email":
        norm_val = normalizers.normalize_email(value)
    elif type == "phone":
        norm_val = normalizers.normalize_phone(value)
    else:
        norm_val = normalizers.normalize_upi(value)
        
    if not norm_val:
        return {"report_count": 0, "risk_level": "low"}
        
    val_hash = normalizers.hash_contact(norm_val)
    
    rep = db.query(models.ContactReputation).filter(
        models.ContactReputation.contact_hash == val_hash
    ).first()
    
    report_count = rep.report_count if rep else 0
    
    if report_count == 0:
        risk_level = "low"
    elif report_count == 1:
        risk_level = "medium"
    else:
        risk_level = "high"
        
    return {"report_count": report_count, "risk_level": risk_level}

@app.get("/api/checks", response_model=schemas.HistoryResponse)
def get_checks(
    db: Session = Depends(get_db),
    user: models.User = Depends(auth.get_current_user)
):
    checks = db.query(models.Check).filter(
        models.Check.user_id == user.id
    ).order_by(models.Check.created_at.desc()).all()
    
    return {"checks": checks}

@app.post("/api/upi/check", response_model=schemas.UpiCheckResponse)
def check_upi(
    req: schemas.UpiCheckRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    check_rate_limit(request)
    from app import upi_detector
    return upi_detector.analyze_upi_transaction(
        upi_id=req.upi_id,
        message_text=req.message_text or "",
        amount=req.amount or "",
        db=db
    )

@app.post("/api/whatsapp/message", response_model=schemas.WhatsAppMessageResponse)
def handle_whatsapp_message(
    req: schemas.WhatsAppMessageRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    check_rate_limit(request)
    from app import whatsapp_bot
    return whatsapp_bot.process_whatsapp_message(
        sender=req.sender or "student",
        message_text=req.message_text,
        db=db
    )

@app.post("/api/analyze/document", response_model=schemas.DocumentAnalyzeResponse)
def analyze_document(
    req: schemas.DocumentAnalyzeRequest,
    request: Request
):
    check_rate_limit(request)
    from app import offer_letter_analyzer
    return offer_letter_analyzer.analyze_offer_letter(
        document_text=req.document_text,
        filename=req.filename or "offer_letter.pdf"
    )

@app.get("/api/fingerprints/search", response_model=schemas.FingerprintSearchResponse)
def search_fingerprint_db(
    query: Optional[str] = "",
    db: Session = Depends(get_db)
):
    from app import fingerprint_engine
    return fingerprint_engine.search_fingerprints(query=query or "", db=db)

@app.get("/api/reports/feed", response_model=schemas.CommunityFeedResponse)
def get_community_feed(
    db: Session = Depends(get_db)
):
    reports = db.query(models.ScamReport).order_by(
        models.ScamReport.created_at.desc()
    ).limit(30).all()
    return {"reports": reports}

@app.post("/api/reports/{report_id}/confirm")
def confirm_report(
    report_id: str,
    db: Session = Depends(get_db)
):
    report = db.query(models.ScamReport).filter(models.ScamReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    report.confirm_count += 1
    db.commit()
    return {"id": report.id, "confirm_count": report.confirm_count}


