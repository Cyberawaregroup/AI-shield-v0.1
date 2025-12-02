from datetime import datetime
from typing import Any, Dict, List, Optional

import orjson as json
from pydantic import BaseModel
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy import orm

from app.core import utils
from app.core.database import Base


class ChatSession(Base):
    __tablename__ = "chat_sessions"
    __table_args__ = (
        Index("ix_chat_sessions_user_id_status", "user_id", "status"),
        Index("ix_chat_sessions_status_risk_level", "status", "risk_level"),
        Index("ix_chat_sessions_created_at_status", "created_at", "status"),
        CheckConstraint(
            "status IN ('active', 'closed', 'escalated', 'archived')",
            name="ck_chat_sessions_status_valid",
        ),
        CheckConstraint(
            "risk_level IN ('low', 'medium', 'high', 'critical')",
            name="ck_chat_sessions_risk_level_valid",
        ),
        CheckConstraint(
            "length(session_id) > 0",
            name="ck_chat_sessions_session_id_not_empty",
        ),
    )

    id: orm.Mapped[int] = orm.mapped_column(Integer, primary_key=True, index=True)
    user_id: orm.Mapped[int | None] = orm.mapped_column(
        Integer, ForeignKey("users.id"), nullable=True, index=True
    )
    session_id: orm.Mapped[str] = orm.mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    status: orm.Mapped[str] = orm.mapped_column(
        String(50), default="active", nullable=False
    )
    risk_level: orm.Mapped[str] = orm.mapped_column(
        String(50), default="low", nullable=False
    )
    vulnerability_factors: orm.Mapped[str] = orm.mapped_column(
        Text, default="[]", nullable=False
    )  # JSON string
    escalation_reason: orm.Mapped[str | None] = orm.mapped_column(Text, nullable=True)
    escalated_to: orm.Mapped[str | None] = orm.mapped_column(String(255), nullable=True)
    escalated_at: orm.Mapped[datetime | None] = orm.mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: orm.Mapped[datetime] = orm.mapped_column(
        DateTime(timezone=True), default=utils.now, nullable=False
    )
    updated_at: orm.Mapped[datetime] = orm.mapped_column(
        DateTime(timezone=True), default=utils.now, onupdate=utils.now, nullable=False
    )

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
        self.vulnerability_factors = json.dumps(value).decode()


class ChatMessage(Base):
    __tablename__ = "chat_messages"
    __table_args__ = (
        Index("ix_chat_messages_session_id_message_type", "session_id", "message_type"),
        Index("ix_chat_messages_created_at_message_type", "created_at", "message_type"),
        Index("ix_chat_messages_ai_model_ai_confidence", "ai_model", "ai_confidence"),
        CheckConstraint(
            "message_type IN ('user', 'assistant', 'system', 'error')",
            name="ck_chat_messages_message_type_valid",
        ),
        CheckConstraint(
            "ai_confidence IS NULL OR (ai_confidence >= 0.0 AND ai_confidence <= 1.0)",
            name="ck_chat_messages_ai_confidence_range",
        ),
        CheckConstraint(
            "length(content) > 0",
            name="ck_chat_messages_content_not_empty",
        ),
        CheckConstraint(
            "user_feedback IS NULL OR user_feedback IN ('positive', 'negative', 'neutral')",
            name="ck_chat_messages_user_feedback_valid",
        ),
    )

    id: orm.Mapped[int] = orm.mapped_column(Integer, primary_key=True, index=True)
    session_id: orm.Mapped[int] = orm.mapped_column(
        Integer, ForeignKey("chat_sessions.id"), index=True, nullable=False
    )
    message_type: orm.Mapped[str] = orm.mapped_column(String(50), nullable=False)
    content: orm.Mapped[str] = orm.mapped_column(Text, nullable=False)
    message_metadata: orm.Mapped[str] = orm.mapped_column(
        Text, default="{}", nullable=False
    )  # JSON string

    # AI-specific fields
    ai_model: orm.Mapped[str | None] = orm.mapped_column(String(100), nullable=True)
    ai_confidence: orm.Mapped[float | None] = orm.mapped_column(Float, nullable=True)
    ai_reasoning: orm.Mapped[str | None] = orm.mapped_column(Text, nullable=True)

    # User interaction
    user_feedback: orm.Mapped[str | None] = orm.mapped_column(String(50), nullable=True)
    is_helpful: orm.Mapped[bool | None] = orm.mapped_column(Boolean, nullable=True)

    # Timestamps
    created_at: orm.Mapped[datetime] = orm.mapped_column(
        DateTime(timezone=True), default=utils.now, nullable=False
    )

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
        self.message_metadata = json.dumps(value).decode()


class FraudReport(Base):
    __tablename__ = "fraud_reports"
    __table_args__ = (
        Index("ix_fraud_reports_user_id_status", "user_id", "status"),
        Index("ix_fraud_reports_fraud_type_risk_level", "fraud_type", "risk_level"),
        Index("ix_fraud_reports_reported_at_status", "reported_at", "status"),
        Index("ix_fraud_reports_status_assigned_to", "status", "assigned_to"),
        CheckConstraint(
            "risk_level IN ('low', 'medium', 'high', 'critical')",
            name="ck_fraud_reports_risk_level_valid",
        ),
        CheckConstraint(
            "status IN ('open', 'investigating', 'resolved', 'closed', 'false_positive')",
            name="ck_fraud_reports_status_valid",
        ),
        CheckConstraint(
            "financial_loss IS NULL OR financial_loss >= 0",
            name="ck_fraud_reports_financial_loss_positive",
        ),
        CheckConstraint(
            "length(fraud_type) > 0",
            name="ck_fraud_reports_fraud_type_not_empty",
        ),
        CheckConstraint(
            "length(description) > 0",
            name="ck_fraud_reports_description_not_empty",
        ),
    )

    id: orm.Mapped[int] = orm.mapped_column(Integer, primary_key=True, index=True)
    user_id: orm.Mapped[int | None] = orm.mapped_column(
        Integer, ForeignKey("users.id"), nullable=True, index=True
    )
    session_id: orm.Mapped[int | None] = orm.mapped_column(
        Integer, ForeignKey("chat_sessions.id"), nullable=True, index=True
    )
    fraud_type: orm.Mapped[str] = orm.mapped_column(String(100), nullable=False)
    description: orm.Mapped[str] = orm.mapped_column(Text, nullable=False)
    risk_level: orm.Mapped[str] = orm.mapped_column(
        String(50), default="medium", nullable=False
    )
    evidence_files: orm.Mapped[str] = orm.mapped_column(
        Text, default="[]", nullable=False
    )  # JSON string
    evidence_links: orm.Mapped[str] = orm.mapped_column(
        Text, default="[]", nullable=False
    )  # JSON string
    financial_loss: orm.Mapped[float | None] = orm.mapped_column(Float, nullable=True)
    reported_at: orm.Mapped[datetime] = orm.mapped_column(
        DateTime(timezone=True), default=utils.now, nullable=False
    )
    status: orm.Mapped[str] = orm.mapped_column(
        String(50), default="open", nullable=False
    )
    assigned_to: orm.Mapped[str | None] = orm.mapped_column(String(255), nullable=True)
    resolution_notes: orm.Mapped[str | None] = orm.mapped_column(Text, nullable=True)
    resolved_at: orm.Mapped[datetime | None] = orm.mapped_column(
        DateTime(timezone=True), nullable=True
    )

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
        self.evidence_files = json.dumps(value).decode()

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
        self.evidence_links = json.dumps(value).decode()


class SecurityAdvisor(Base):
    __tablename__ = "security_advisors"
    __table_args__ = (
        Index(
            "ix_security_advisors_is_available_current_load",
            "is_available",
            "current_load",
        ),
        Index("ix_security_advisors_email_is_available", "email", "is_available"),
        CheckConstraint(
            "experience_years >= 0",
            name="ck_security_advisors_experience_years_positive",
        ),
        CheckConstraint(
            "current_load >= 0",
            name="ck_security_advisors_current_load_positive",
        ),
        CheckConstraint(
            "max_load > 0",
            name="ck_security_advisors_max_load_positive",
        ),
        CheckConstraint(
            "current_load <= max_load",
            name="ck_security_advisors_current_load_lte_max",
        ),
        CheckConstraint(
            "length(name) > 0",
            name="ck_security_advisors_name_not_empty",
        ),
        CheckConstraint(
            "length(email) > 0",
            name="ck_security_advisors_email_not_empty",
        ),
    )

    id: orm.Mapped[int] = orm.mapped_column(Integer, primary_key=True, index=True)
    name: orm.Mapped[str] = orm.mapped_column(String(255), nullable=False)
    email: orm.Mapped[str] = orm.mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    phone: orm.Mapped[str | None] = orm.mapped_column(String(20), nullable=True)
    specialization: orm.Mapped[str] = orm.mapped_column(
        Text, default="[]", nullable=False
    )  # JSON string
    certifications: orm.Mapped[str] = orm.mapped_column(
        Text, default="[]", nullable=False
    )  # JSON string
    experience_years: orm.Mapped[int] = orm.mapped_column(
        Integer, default=0, nullable=False
    )
    is_available: orm.Mapped[bool] = orm.mapped_column(
        Boolean, default=True, nullable=False
    )
    current_load: orm.Mapped[int] = orm.mapped_column(
        Integer, default=0, nullable=False
    )
    max_load: orm.Mapped[int] = orm.mapped_column(Integer, default=10, nullable=False)
    available_hours: orm.Mapped[str] = orm.mapped_column(
        Text, default="{}", nullable=False
    )  # JSON string
    created_at: orm.Mapped[datetime] = orm.mapped_column(
        DateTime(timezone=True), default=utils.now, nullable=False
    )
    updated_at: orm.Mapped[datetime] = orm.mapped_column(
        DateTime(timezone=True), default=utils.now, onupdate=utils.now, nullable=False
    )

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
        self.specialization = json.dumps(value).decode()

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
        self.certifications = json.dumps(value).decode()

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
        self.available_hours = json.dumps(value).decode()


