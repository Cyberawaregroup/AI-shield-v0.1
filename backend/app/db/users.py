import datetime
from typing import List

import orjson as json
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Float,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy import orm

from app.core import utils
from app.core.db import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        Index("ix_users_email_is_active", "email", "is_active"),
        Index("ix_users_role_is_active", "role", "is_active"),
        Index("ix_users_is_vulnerable_risk_score", "is_vulnerable", "risk_score"),
        CheckConstraint("age IS NULL OR age > 0", name="ck_users_age_positive"),
        CheckConstraint(
            "vulnerability_score >= 0.0 AND vulnerability_score <= 100.0",
            name="ck_users_vulnerability_score_range",
        ),
        CheckConstraint(
            "risk_score >= 0.0 AND risk_score <= 100.0",
            name="ck_users_risk_score_range",
        ),
        CheckConstraint("total_breaches >= 0", name="ck_users_total_breaches_positive"),
        CheckConstraint(
            "total_phishing_attempts >= 0",
            name="ck_users_total_phishing_attempts_positive",
        ),
        CheckConstraint("length(email) > 0", name="ck_users_email_not_empty"),
        CheckConstraint("length(name) > 0", name="ck_users_name_not_empty"),
    )

    id: orm.Mapped[int] = orm.mapped_column(Integer, primary_key=True, index=True)
    email: orm.Mapped[str] = orm.mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    phone: orm.Mapped[str | None] = orm.mapped_column(String(20), nullable=True)
    name: orm.Mapped[str] = orm.mapped_column(String(255), nullable=False)
    role: orm.Mapped[str] = orm.mapped_column(
        String(50), default="user", nullable=False
    )
    hashed_password: orm.Mapped[str] = orm.mapped_column(String(255), nullable=False)
    is_active: orm.Mapped[bool] = orm.mapped_column(
        Boolean, default=True, nullable=False
    )

    # Vulnerability assessment
    age: orm.Mapped[int | None] = orm.mapped_column(Integer, nullable=True)
    is_vulnerable: orm.Mapped[bool] = orm.mapped_column(
        Boolean, default=False, nullable=False
    )
    vulnerability_factors: orm.Mapped[str] = orm.mapped_column(
        Text, default="[]", nullable=False
    )  # JSON string
    vulnerability_score: orm.Mapped[float] = orm.mapped_column(
        Float, default=0.0, nullable=False
    )

    # Security metrics
    risk_score: orm.Mapped[float] = orm.mapped_column(
        Float, default=0.0, nullable=False
    )
    total_breaches: orm.Mapped[int] = orm.mapped_column(
        Integer, default=0, nullable=False
    )
    total_phishing_attempts: orm.Mapped[int] = orm.mapped_column(
        Integer, default=0, nullable=False
    )
    created_at: orm.Mapped[datetime.datetime] = orm.mapped_column(
        DateTime(timezone=True), default=utils.now, nullable=False
    )
    updated_at: orm.Mapped[datetime.datetime] = orm.mapped_column(
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
