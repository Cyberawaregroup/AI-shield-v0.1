from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime, date
from enum import Enum

# Enums (same as database enums)
class ScamTypeEnum(str, Enum):
    PHISHING_EMAIL = "phishing_email"
    PHISHING_TEXT = "phishing_text"
    FAKE_WEBSITE = "fake_website"
    INVESTMENT_SCAM = "investment_scam"
    TECH_SUPPORT_SCAM = "tech_support_scam"
    ROMANCE_SCAM = "romance_scam"
    JOB_SCAM = "job_scam"
    IMPERSONATION = "impersonation"
    OTHER = "other"

class AgeGroupEnum(str, Enum):
    UNDER_18 = "under_18"
    AGE_18_24 = "18_24"
    AGE_25_34 = "25_34"
    AGE_35_44 = "35_44"
    AGE_45_54 = "45_54"
    AGE_55_64 = "55_64"
    AGE_65_PLUS = "65_plus"

class PaymentMethodEnum(str, Enum):
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    WIRE_TRANSFER = "wire_transfer"
    CRYPTOCURRENCY = "cryptocurrency"
    CASH = "cash"
    GIFT_CARDS = "gift_cards"
    BANK_TRANSFER = "bank_transfer"
    PAYPAL = "paypal"
    OTHER = "other"

# Input models for form submission
class ScamReportCreate(BaseModel):
    # Reporter Information (Optional)
    reporter_name: Optional[str] = Field(None, max_length=255)
    reporter_email: Optional[EmailStr] = None
    reporter_phone: Optional[str] = Field(None, max_length=50)
    
    # Scam Details (Required)
    incident_date: date = Field(..., description="Date when the scam occurred")
    incident_time: Optional[str] = Field(None, pattern=r"^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$")  # FIXED: changed regex= to pattern=
    scam_type: ScamTypeEnum = Field(..., description="Type of scam")
    other_scam_type: Optional[str] = Field(None, max_length=255)
    description: str = Field(..., min_length=10, max_length=1000, description="Brief description of what happened")
    how_scam_began: Optional[str] = Field(None, max_length=500, description="How did the scam begin?")
    
    # Financial Impact
    money_lost: bool = Field(False, description="Was any money lost?")
    amount_lost: Optional[float] = Field(None, ge=0, description="Amount lost if any")
    payment_method: Optional[PaymentMethodEnum] = None
    
    # Scammer Contact Information
    scammer_email: Optional[EmailStr] = None
    scammer_phone: Optional[str] = Field(None, max_length=50)
    scammer_website: Optional[str] = Field(None, max_length=500)
    scammer_social_media: Optional[str] = Field(None, max_length=500)
    
    # Victim Information (Optional)
    is_reporter_victim: bool = Field(True, description="Are you the target/victim?")
    victim_relation: Optional[str] = Field(None, max_length=100)
    victim_age_group: Optional[AgeGroupEnum] = None
    
    # Consent
    information_accurate: bool = Field(..., description="Confirm information is accurate")
    consent_to_contact: bool = Field(False, description="Consent to being contacted for follow-up")

    @validator('other_scam_type')
    def validate_other_scam_type(cls, v, values):
        if values.get('scam_type') == ScamTypeEnum.OTHER and not v:
            raise ValueError('Other scam type description is required when scam type is "other"')
        return v

    @validator('amount_lost')
    def validate_amount_lost(cls, v, values):
        if values.get('money_lost') and v is None:
            raise ValueError('Amount lost is required when money was lost')
        if values.get('money_lost') and v is not None and v <= 0:
            raise ValueError('Amount lost must be greater than 0')
        return v

    @validator('payment_method')
    def validate_payment_method(cls, v, values):
        if values.get('money_lost') and not v:
            raise ValueError('Payment method is required when money was lost')
        return v

    @validator('victim_relation')
    def validate_victim_relation(cls, v, values):
        if not values.get('is_reporter_victim') and not v:
            raise ValueError('Victim relation is required when reporter is not the victim')
        return v

    @validator('incident_date')
    def validate_incident_date(cls, v):
        if v > date.today():
            raise ValueError('Incident date cannot be in the future')
        return v

class ScamReportResponse(BaseModel):
    id: int
    reporter_name: Optional[str]
    reporter_email: Optional[str]
    reporter_phone: Optional[str]
    incident_date: date
    incident_time: Optional[str]
    scam_type: ScamTypeEnum
    other_scam_type: Optional[str]
    description: str
    how_scam_began: Optional[str]
    money_lost: bool
    amount_lost: Optional[float]
    payment_method: Optional[PaymentMethodEnum]
    scammer_email: Optional[str]
    scammer_phone: Optional[str]
    scammer_website: Optional[str]
    scammer_social_media: Optional[str]
    is_reporter_victim: bool
    victim_relation: Optional[str]
    victim_age_group: Optional[AgeGroupEnum]
    information_accurate: bool
    consent_to_contact: bool
    status: str
    created_at: datetime
    evidence_files: List['EvidenceFileResponse'] = []

    class Config:
        from_attributes = True

class EvidenceFileResponse(BaseModel):
    id: int
    filename: str
    original_filename: str
    file_size: int
    file_type: str
    uploaded_at: datetime

    class Config:
        from_attributes = True

# Update the forward reference
ScamReportResponse.model_rebuild()

class ScamReportSummary(BaseModel):
    id: int
    scam_type: ScamTypeEnum
    incident_date: date
    money_lost: bool
    amount_lost: Optional[float]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class ScamReportStats(BaseModel):
    total_reports: int
    reports_with_financial_loss: int
    total_amount_lost: float
    most_common_scam_types: List[dict]
    reports_by_status: dict
