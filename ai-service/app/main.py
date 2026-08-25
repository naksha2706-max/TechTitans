"""
Run:
    uvicorn app.main:app --reload --port 8100

This service implements the rule-based scoring engine from
docs/FEATURE_SPECIFICATION.md. The backend (Phase 1-2) calls this over
HTTP from its own POST /api/analyze handler, per AGENTS.md rule 12
(backend and ai-service stay independent — backend must run even if
ai-service is down, by falling back or returning a clear error).
"""

from fastapi import FastAPI

from .rules.scorer import analyze
from .schemas import AnalyzeRequest, AnalyzeResponse

app = FastAPI(title="Scam Detector AI Service", version="0.1.0")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze_endpoint(req: AnalyzeRequest) -> AnalyzeResponse:
    result = analyze(
        req.message_text,
        company_name=req.company_name,
        salary=req.salary,
        website=req.website,
        contact_email=req.contact_email,
        reputation_hit_count=req.reputation_hit_count,
    )
    return AnalyzeResponse(**result.to_dict())
