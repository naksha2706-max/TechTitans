from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from uuid import UUID
from datetime import datetime

# --- Auth ---
class AuthRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# --- Analysis ---
class AnalyzeRequest(BaseModel):
    company_name: Optional[str] = None
    message_text: str = Field(..., max_length=5000)
    salary: Optional[str] = None
    website: Optional[str] = None
    contact_email: Optional[str] = None

class WarningDetail(BaseModel):
    code: str
    label: str
    points: int

class AnalyzeResponse(BaseModel):
    risk_score: int
    risk_band: str
    warnings: List[WarningDetail]
    recommendation: str

# --- Reports ---
class ReportRequest(BaseModel):
    company_name: Optional[str] = None
    description: str = Field(..., max_length=5000)
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_upi: Optional[str] = None

class ReportResponse(BaseModel):
    id: UUID
    status: str

# --- Reputation ---
class ReputationResponse(BaseModel):
    report_count: int
    risk_level: str

# --- History ---
class CheckHistoryItem(BaseModel):
    id: UUID
    company_name: Optional[str] = None
    message_text: str
    salary: Optional[str] = None
    website: Optional[str] = None
    contact_email: Optional[str] = None
    risk_score: int
    risk_band: str
    warnings: List[WarningDetail]
    created_at: datetime

    class Config:
        from_attributes = True

class HistoryResponse(BaseModel):
    checks: List[CheckHistoryItem]
