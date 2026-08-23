import uuid
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Uuid, JSON
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

class Check(Base):
    __tablename__ = "checks"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id = Column(Uuid, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    company_name = Column(String, nullable=True)
    message_text = Column(String, nullable=False)
    salary = Column(String, nullable=True)
    website = Column(String, nullable=True)
    contact_email = Column(String, nullable=True)
    risk_score = Column(Integer, nullable=False)
    risk_band = Column(String, nullable=False)
    warnings = Column(JSON, nullable=False, default=list)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

class ScamReport(Base):
    __tablename__ = "scam_reports"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id = Column(Uuid, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    company_name = Column(String, nullable=True)
    description = Column(String, nullable=False)
    contact_email_hash = Column(String, nullable=True)
    contact_phone_hash = Column(String, nullable=True)
    contact_upi_hash = Column(String, nullable=True)
    status = Column(String, nullable=False, default="pending")
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

class ContactReputation(Base):
    __tablename__ = "contact_reputation"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    contact_hash = Column(String, unique=True, nullable=False, index=True)
    contact_type = Column(String, nullable=False)
    report_count = Column(Integer, nullable=False, default=0)
    last_reported_at = Column(DateTime(timezone=True), nullable=True)
