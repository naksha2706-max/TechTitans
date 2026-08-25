from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    message_text: str = Field(..., min_length=1, max_length=5000)
    company_name: str | None = None
    salary: str | None = None
    website: str | None = None
    contact_email: str | None = None
    reputation_hit_count: int = 0  # backend fills this in from contact_reputation lookup


class Warning(BaseModel):
    code: str
    points: int
    label: str


class AnalyzeResponse(BaseModel):
    risk_score: int
    risk_band: str
    warnings: list[Warning]
    recommendation: str
