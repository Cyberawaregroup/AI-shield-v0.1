from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
import json

Base = declarative_base()

class ChatSessionStatus(str, Enum):
    ACTIVE = "active"
    ESCALATED = "escalated"
    CLOSED = "closed"
    ARCHIVED = "archived"

class MessageType(str, Enum):
    USER = "user"
    BOT = "bot"
    ADVISOR = "advisor"
    SYSTEM = "system"

class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class FraudType(str, Enum):
    PHISHING = "phishing"
    SOCIAL_ENGINEERING = "social_engineering"
    IDENTITY_THEFT = "identity_theft"
    FINANCIAL_FRAUD = "financial_fraud"
    TECH_SUPPORT_SCAM = "tech_support_scam"
    OTHER = "other"

class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    session_id = Column(String, unique=True, index=True)
    status = Column(String, default="active")
    risk_level = Column(String, default="low")
    vulnerability_factors = Column(Text, default="[]")  # JSON string
    escalation_reason = Column(Text, nullable=True)
    escalated_to = Column(String, nullable=True)
    escalated_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def vulnerability_factors_list(self) -> List[str]:
        """Get vulnerability factors as a list"""
        try:
            return json.loads(self.vulnerability_factors)
        except (json.JSONDecodeError, TypeError):
            return []

    @vulnerability_factors_list.setter
    def vulnerability_factors_list(self, value: List[str]):
        """Set vulnerability factors from a list"""
        self.vulnerability_factors = json.dumps(value)

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"), index=True)
    message_type = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    message_metadata = Column(Text, default="{}")  # JSON string instead of Dict[str, Any]

    # AI-specific fields
    ai_model = Column(String, nullable=True)
    ai_confidence = Column(Float, nullable=True)
    ai_reasoning = Column(Text, nullable=True)

    # User interaction
    user_feedback = Column(String, nullable=True)
    is_helpful = Column(Boolean, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)

    @property
    def metadata_dict(self) -> Dict[str, Any]:
        """Get metadata as a dictionary"""
        try:
            return json.loads(self.message_metadata)
        except (json.JSONDecodeError, TypeError):
            return {}

    @metadata_dict.setter
    def metadata_dict(self, value: Dict[str, Any]):
        """Set metadata from a dictionary"""
        self.message_metadata = json.dumps(value)

class FraudReport(Base):
    __tablename__ = "fraud_reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=True, index=True)
    fraud_type = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    risk_level = Column(String, default="medium")
    evidence_files = Column(Text, default="[]")  # JSON string
    evidence_links = Column(Text, default="[]")  # JSON string
    financial_loss = Column(Float, nullable=True)
    reported_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="open")
    assigned_to = Column(String, nullable=True)
    resolution_notes = Column(Text, nullable=True)
    resolved_at = Column(DateTime, nullable=True)

    @property
    def evidence_files_list(self) -> List[str]:
        """Get evidence files as a list"""
        try:
            return json.loads(self.evidence_files)
        except (json.JSONDecodeError, TypeError):
            return []

    @evidence_files_list.setter
    def evidence_files_list(self, value: List[str]):
        """Set evidence files from a list"""
        self.evidence_files = json.dumps(value)

    @property
    def evidence_links_list(self) -> List[str]:
        """Get evidence links as a list"""
        try:
            return json.loads(self.evidence_links)
        except (json.JSONDecodeError, TypeError):
            return []

    @evidence_links_list.setter
    def evidence_links_list(self, value: List[str]):
        """Set evidence links from a list"""
        self.evidence_links = json.dumps(value)

class SecurityAdvisor(Base):
    __tablename__ = "security_advisors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    phone = Column(String, nullable=True)
    specialization = Column(Text, default="[]")  # JSON string
    certifications = Column(Text, default="[]")  # JSON string
    experience_years = Column(Integer, default=0)
    is_available = Column(Boolean, default=True)
    current_load = Column(Integer, default=0)
    max_load = Column(Integer, default=10)
    available_hours = Column(Text, default="{}")  # JSON string
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def specialization_list(self) -> List[str]:
        """Get specialization as a list"""
        try:
            return json.loads(self.specialization)
        except (json.JSONDecodeError, TypeError):
            return []

    @specialization_list.setter
    def specialization_list(self, value: List[str]):
        """Set specialization from a list"""
        self.specialization = json.dumps(value)

    @property
    def certifications_list(self) -> List[str]:
        """Get certifications as a list"""
        try:
            return json.loads(self.certifications)
        except (json.JSONDecodeError, TypeError):
            return []

    @certifications_list.setter
    def certifications_list(self, value: List[str]):
        """Set certifications from a list"""
        self.certifications = json.dumps(value)

    @property
    def available_hours_dict(self) -> Dict[str, List[str]]:
        """Get available hours as a dictionary"""
        try:
            return json.loads(self.available_hours)
        except (json.JSONDecodeError, TypeError):
            return {}

    @available_hours_dict.setter
    def available_hours_dict(self, value: Dict[str, List[str]]):
        """Set available hours from a dictionary"""
        self.available_hours = json.dumps(value)

# Pydantic models for API requests/responses
class ChatMessageCreate(BaseModel):
    content: str
    message_type: str = "user"
    message_metadata: Optional[Dict[str, Any]] = {}

class ChatMessageResponse(BaseModel):
    id: int
    message_type: str
    content: str
    message_metadata: Dict[str, Any]
    ai_model: Optional[str] = None
    ai_confidence: Optional[float] = None
    ai_reasoning: Optional[str] = None
    created_at: datetime

class ChatSessionCreate(BaseModel):
    user_id: Optional[int] = None
    vulnerability_factors: Optional[List[str]] = []

class ChatSessionResponse(BaseModel):
    id: int
    session_id: str
    status: str
    risk_level: str
    vulnerability_factors: List[str]
    created_at: datetime

class FraudReportCreate(BaseModel):
    fraud_type: str
    description: str
    risk_level: str = "medium"
    evidence_files: Optional[List[str]] = []
    evidence_links: Optional[List[str]] = []
    financial_loss: Optional[float] = None

class FraudReportResponse(BaseModel):
    id: int
    fraud_type: str
    description: str
    risk_level: str
    evidence_files: List[str]
    evidence_links: List[str]
    financial_loss: Optional[float] = None
    status: str
    reported_at: datetime
