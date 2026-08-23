import hashlib
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app import models, normalizers

def generate_text_fingerprint(text: str) -> str:
    """Generates a SHA-256 fingerprint for a normalized text string."""
    cleaned = " ".join((text or "").lower().split())
    return hashlib.sha256(cleaned.encode("utf-8")).hexdigest()

def search_fingerprints(query: str, db: Session) -> Dict[str, Any]:
    """
    Searches contact reputation records, report entries, and pattern fingerprints
    matching the search query (email, phone, UPI ID, or URL domain).
    """
    if not query or not query.strip():
        # Return latest reputation entries if query is empty
        reputations = db.query(models.ContactReputation).order_by(
            models.ContactReputation.report_count.desc()
        ).limit(10).all()
        
        return {
            "query": "",
            "matches_found": len(reputations),
            "fingerprints": [
                {
                    "contact_hash": r.contact_hash,
                    "type": r.contact_type,
                    "report_count": r.report_count,
                    "last_reported_at": r.last_reported_at.isoformat() if r.last_reported_at else None
                }
                for r in reputations
            ]
        }

    query_norm = query.strip()
    query_hash = normalizers.hash_contact(query_norm)

    # 1. Search reputation table
    rep = db.query(models.ContactReputation).filter(
        models.ContactReputation.contact_hash == query_hash
    ).first()

    # 2. Search scam reports by company name
    reports = db.query(models.ScamReport).filter(
        models.ScamReport.company_name.ilike(f"%{query_norm}%")
    ).all()

    fingerprints = []
    if rep:
        fingerprints.append({
            "contact_hash": rep.contact_hash,
            "type": rep.contact_type,
            "report_count": rep.report_count,
            "last_reported_at": rep.last_reported_at.isoformat() if rep.last_reported_at else None,
            "matched_by": "exact_contact_hash"
        })

    for r in reports:
        fingerprints.append({
            "contact_hash": r.contact_email_hash or r.contact_phone_hash or r.contact_upi_hash or "text_hash",
            "company_name": r.company_name,
            "description": r.description,
            "status": r.status,
            "created_at": r.created_at.isoformat() if r.created_at else None,
            "matched_by": "company_name"
        })

    return {
        "query": query_norm,
        "matches_found": len(fingerprints),
        "fingerprints": fingerprints
    }
