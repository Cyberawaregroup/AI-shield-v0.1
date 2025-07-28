from sqlalchemy import Column, Integer, String, Text, Boolean, Float, Date, Time, DateTime, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
# from model import engine
import enum

# Import the Base and User from your existing model.py
from model import Base, User, engine

# Define the enums
class ScamType(enum.Enum):
    PHISHING = "phishing"
    FAKE_WEBSITE = "fake_website"
    INVESTMENT = "investment"
    TECH_SUPPORT = "tech_support"
    ROMANCE = "romance"
    JOB = "job"
    IMPERSONATION = "impersonation"
    OTHER = "other"

class PaymentMethod(enum.Enum):
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    BANK_TRANSFER = "bank_transfer"
    WIRE_TRANSFER = "wire_transfer"
    CRYPTOCURRENCY = "cryptocurrency"
    CASH = "cash"
    CHECK = "check"
    MONEY_ORDER = "money_order"
    GIFT_CARD = "gift_card"
    MOBILE_PAYMENT = "mobile_payment"
    OTHER = "other"

class AgeGroup(enum.Enum):
    UNDER_18 = "under_18"
    AGE_18_24 = "18_24"
    AGE_25_34 = "25_34"
    AGE_35_44 = "35_44"
    AGE_45_54 = "45_54"
    AGE_55_64 = "55_64"
    AGE_65_PLUS = "65_plus"

class ReportStatus(enum.Enum):
    PENDING = "pending"
    UNDER_REVIEW = "under_review"
    INVESTIGATED = "investigated"
    CLOSED = "closed"

class ScamReport(Base):
    __tablename__ = "scam_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Reporter Information
    reporter_name = Column(String(255), nullable=True)
    reporter_email = Column(String(255), nullable=True)
    reporter_phone = Column(String(50), nullable=True)
    
    # Scam Details
    incident_date = Column(Date, nullable=False)
    incident_time = Column(String(5), nullable=True)  # HH:MM format
    scam_type = Column(Enum(ScamType), nullable=False)
    other_scam_type = Column(String(255), nullable=True)
    description = Column(Text, nullable=False)
    how_scam_began = Column(String(500), nullable=True)
    
    # Financial Impact
    money_lost = Column(Boolean, default=False)
    amount_lost = Column(Float, nullable=True)
    payment_method = Column(Enum(PaymentMethod), nullable=True)
    
    # Scammer Contact Info
    scammer_email = Column(String(255), nullable=True)
    scammer_phone = Column(String(50), nullable=True)
    scammer_website = Column(String(500), nullable=True)
    scammer_social_media = Column(String(255), nullable=True)
    
    # Victim Information
    is_reporter_victim = Column(Boolean, default=True)
    victim_relation = Column(String(100), nullable=True)
    victim_age_group = Column(Enum(AgeGroup), nullable=True)
    
    # Consent
    information_accurate = Column(Boolean, nullable=False)
    consent_to_contact = Column(Boolean, default=False)
    
    # System fields
    status = Column(Enum(ReportStatus), default=ReportStatus.PENDING)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Optional for anonymous reports
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="scam_reports")
    evidence_files = relationship("ScamEvidence", back_populates="scam_report", cascade="all, delete-orphan")

class ScamEvidence(Base):
    __tablename__ = "scam_evidence"
    
    id = Column(Integer, primary_key=True, index=True)
    scam_report_id = Column(Integer, ForeignKey("scam_reports.id"), nullable=False)
    
    # File information
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=False)
    file_type = Column(String(100), nullable=False)
    mime_type = Column(String(100), nullable=False)
    
    # Timestamps
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    scam_report = relationship("ScamReport", back_populates="evidence_files")

# Update the User model to include relationship with scam reports
# Add this to your existing User class in model.py or modify here
# User.scam_reports = relationship("ScamReport", back_populates="user")
Base.metadata.create_all(bind=engine)