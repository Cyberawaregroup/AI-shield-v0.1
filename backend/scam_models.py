
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()

class ScamType(enum.Enum):
    PHISHING_EMAIL = "phishing_email"
    PHISHING_TEXT = "phishing_text" 
    FAKE_WEBSITE = "fake_website"
    INVESTMENT_SCAM = "investment_scam"
    TECH_SUPPORT_SCAM = "tech_support_scam"
    ROMANCE_SCAM = "romance_scam"
    JOB_SCAM = "job_scam"
    IMPERSONATION = "impersonation"
    OTHER = "other"

class AgeGroup(enum.Enum):
    UNDER_18 = "under_18"
    AGE_18_24 = "18_24"
    AGE_25_34 = "25_34"
    AGE_35_44 = "35_44"
    AGE_45_54 = "45_54"
    AGE_55_64 = "55_64"
    AGE_65_PLUS = "65_plus"

class PaymentMethod(enum.Enum):
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    WIRE_TRANSFER = "wire_transfer"
    CRYPTOCURRENCY = "cryptocurrency"
    CASH = "cash"
    GIFT_CARDS = "gift_cards"
    BANK_TRANSFER = "bank_transfer"
    PAYPAL = "paypal"
    OTHER = "other"

class ScamReport(Base):
    __tablename__ = "scam_reports"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Reporter Information (Optional)
    reporter_name = Column(String(255), nullable=True)
    reporter_email = Column(String(255), nullable=True)
    reporter_phone = Column(String(50), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # If logged in

    # Scam Details (Required)
    incident_date = Column(DateTime, nullable=False)
    incident_time = Column(String(10), nullable=True)  # Format: "HH:MM"
    scam_type = Column(Enum(ScamType), nullable=False)
    other_scam_type = Column(String(255), nullable=True)  # If scam_type is OTHER
    description = Column(Text, nullable=False)  # 300-1000 characters
    how_scam_began = Column(String(500), nullable=True)

    # Financial Impact
    money_lost = Column(Boolean, default=False, nullable=False)
    amount_lost = Column(Float, nullable=True)
    payment_method = Column(Enum(PaymentMethod), nullable=True)

    # Scammer Contact Information
    scammer_email = Column(String(255), nullable=True)
    scammer_phone = Column(String(50), nullable=True)
    scammer_website = Column(String(500), nullable=True)
    scammer_social_media = Column(String(500), nullable=True)

    # Victim Information (Optional)
    is_reporter_victim = Column(Boolean, default=True, nullable=False)
    victim_relation = Column(String(100), nullable=True)  # If not the victim
    victim_age_group = Column(Enum(AgeGroup), nullable=True)

    # Consent and Metadata
    information_accurate = Column(Boolean, default=False, nullable=False)
    consent_to_contact = Column(Boolean, default=False, nullable=False)

    # System fields
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    status = Column(String(50), default="pending", nullable=False)  # pending, investigating, resolved

    # Relationships
    user = relationship("User", back_populates="scam_reports")
    evidence_files = relationship("ScamEvidence", back_populates="scam_report", cascade="all, delete-orphan")

class ScamEvidence(Base):
    __tablename__ = "scam_evidence"

    id = Column(Integer, primary_key=True, index=True)
    scam_report_id = Column(Integer, ForeignKey("scam_reports.id"), nullable=False)

    # File Information
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=False)  # in bytes
    file_type = Column(String(100), nullable=False)  # MIME type

    # Metadata
    uploaded_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship
    scam_report = relationship("ScamReport", back_populates="evidence_files")

# Update the existing User model to include relationship
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    email = Column(String(255), nullable=True)
    full_name = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)

    # Relationship
    scam_reports = relationship("ScamReport", back_populates="user")
