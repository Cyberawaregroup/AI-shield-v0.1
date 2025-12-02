from datetime import datetime
from typing import List, Optional

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


class BreachExposure(Base):
    __tablename__ = "breach_exposures"
    __table_args__ = (
        Index("ix_breach_exposures_user_id_severity", "user_id", "severity"),
        Index("ix_breach_exposures_breach_date_severity", "breach_date", "severity"),
        Index("ix_breach_exposures_source_source_id", "source", "source_id"),
        CheckConstraint(
            "severity IN ('low', 'medium', 'high', 'critical')",
            name="ck_breach_exposures_severity_valid",
        ),
        CheckConstraint(
            "length(breach_name) > 0",
            name="ck_breach_exposures_breach_name_not_empty",
        ),
    )

    id: orm.Mapped[int] = orm.mapped_column(Integer, primary_key=True, index=True)
    breach_name: orm.Mapped[str] = orm.mapped_column(String(255), nullable=False)
    breach_date: orm.Mapped[datetime] = orm.mapped_column(
        DateTime(timezone=True), nullable=False
    )
    breach_description: orm.Mapped[str | None] = orm.mapped_column(Text, nullable=True)
    data_classes: orm.Mapped[str] = orm.mapped_column(
        Text, default="[]", nullable=False
    )  # JSON string
    severity: orm.Mapped[str] = orm.mapped_column(
        String(50), default="medium", nullable=False
    )
    source: orm.Mapped[str] = orm.mapped_column(
        String(100), default="hibp", nullable=False
    )
    source_id: orm.Mapped[str | None] = orm.mapped_column(String(255), nullable=True)
    user_id: orm.Mapped[int | None] = orm.mapped_column(
        Integer, ForeignKey("users.id"), nullable=True, index=True
    )
    created_at: orm.Mapped[datetime] = orm.mapped_column(
        DateTime(timezone=True), default=utils.now, nullable=False
    )

    @property
    def data_classes_list(self) -> List[str]:
        """Get data classes as a list"""
        try:
            return json.loads(self.data_classes)
        except (json.JSONDecodeError, TypeError):
            return []

    @data_classes_list.setter
    def data_classes_list(self, value: List[str]):
        """Set data classes from a list"""
        self.data_classes = json.dumps(value).decode()


class IOC(Base):
    __tablename__ = "indicators_of_compromise"
    __table_args__ = (
        Index("ix_ioc_value_type", "value", "type"),
        Index("ix_ioc_type_severity", "type", "severity"),
        Index("ix_ioc_source_source_id", "source", "source_id"),
        Index("ix_ioc_last_seen_severity", "last_seen", "severity"),
        CheckConstraint(
            "severity IN ('low', 'medium', 'high', 'critical')",
            name="ck_ioc_severity_valid",
        ),
        CheckConstraint(
            "confidence_score >= 0.0 AND confidence_score <= 1.0",
            name="ck_ioc_confidence_score_range",
        ),
        CheckConstraint(
            "sighting_count >= 0",
            name="ck_ioc_sighting_count_positive",
        ),
        CheckConstraint(
            "length(value) > 0",
            name="ck_ioc_value_not_empty",
        ),
        CheckConstraint(
            "length(threat_name) > 0",
            name="ck_ioc_threat_name_not_empty",
        ),
    )

    id: orm.Mapped[int] = orm.mapped_column(Integer, primary_key=True, index=True)
    value: orm.Mapped[str] = orm.mapped_column(String(500), nullable=False, index=True)
    type: orm.Mapped[str] = orm.mapped_column(String(50), nullable=False)
    threat_name: orm.Mapped[str] = orm.mapped_column(String(255), nullable=False)
    description: orm.Mapped[str | None] = orm.mapped_column(Text, nullable=True)
    severity: orm.Mapped[str] = orm.mapped_column(
        String(50), default="medium", nullable=False
    )
    confidence_score: orm.Mapped[float] = orm.mapped_column(
        Float, default=0.0, nullable=False
    )
    tags: orm.Mapped[str] = orm.mapped_column(
        Text, default="[]", nullable=False
    )  # JSON string
    threat_categories: orm.Mapped[str] = orm.mapped_column(
        Text, default="[]", nullable=False
    )  # JSON string
    source: orm.Mapped[str] = orm.mapped_column(
        String(100), default="manual", nullable=False
    )
    source_id: orm.Mapped[str | None] = orm.mapped_column(String(255), nullable=True)
    first_seen: orm.Mapped[datetime] = orm.mapped_column(
        DateTime(timezone=True), default=utils.now, nullable=False
    )
    last_seen: orm.Mapped[datetime] = orm.mapped_column(
        DateTime(timezone=True), default=utils.now, nullable=False
    )
    sighting_count: orm.Mapped[int] = orm.mapped_column(
        Integer, default=1, nullable=False
    )
    created_at: orm.Mapped[datetime] = orm.mapped_column(
        DateTime(timezone=True), default=utils.now, nullable=False
    )
    updated_at: orm.Mapped[datetime] = orm.mapped_column(
        DateTime(timezone=True), default=utils.now, onupdate=utils.now, nullable=False
    )

    @property
    def tags_list(self) -> List[str]:
        """Get tags as a list"""
        try:
            return json.loads(self.tags)
        except (json.JSONDecodeError, TypeError):
            return []

    @tags_list.setter
    def tags_list(self, value: List[str]):
        """Set tags from a list"""
        self.tags = json.dumps(value).decode()

    @property
    def threat_categories_list(self) -> List[str]:
        """Get threat categories as a list"""
        try:
            return json.loads(self.threat_categories)
        except (json.JSONDecodeError, TypeError):
            return []

    @threat_categories_list.setter
    def threat_categories_list(self, value: List[str]):
        """Set threat categories from a list"""
        self.threat_categories = json.dumps(value).decode()


class ThreatFeed(Base):
    __tablename__ = "threat_feeds"
    __table_args__ = (
        Index("ix_threat_feeds_is_active_feed_type", "is_active", "feed_type"),
        Index("ix_threat_feeds_last_updated", "last_updated"),
        CheckConstraint(
            "length(name) > 0",
            name="ck_threat_feeds_name_not_empty",
        ),
        CheckConstraint(
            "length(feed_type) > 0",
            name="ck_threat_feeds_feed_type_not_empty",
        ),
    )

    id: orm.Mapped[int] = orm.mapped_column(Integer, primary_key=True, index=True)
    name: orm.Mapped[str] = orm.mapped_column(String(255), nullable=False)
    description: orm.Mapped[str | None] = orm.mapped_column(Text, nullable=True)
    source_url: orm.Mapped[str | None] = orm.mapped_column(String(500), nullable=True)
    feed_type: orm.Mapped[str] = orm.mapped_column(String(100), nullable=False)
    is_active: orm.Mapped[bool] = orm.mapped_column(
        Boolean, default=True, nullable=False
    )
    last_updated: orm.Mapped[datetime] = orm.mapped_column(
        DateTime(timezone=True), default=utils.now, nullable=False
    )
    created_at: orm.Mapped[datetime] = orm.mapped_column(
        DateTime(timezone=True), default=utils.now, nullable=False
    )


class ThreatAlert(Base):
    __tablename__ = "threat_alerts"
    __table_args__ = (
        Index("ix_threat_alerts_is_active_severity", "is_active", "severity"),
        Index("ix_threat_alerts_threat_type_severity", "threat_type", "severity"),
        Index(
            "ix_threat_alerts_resolution_status_is_active",
            "resolution_status",
            "is_active",
        ),
        Index(
            "ix_threat_alerts_is_acknowledged_is_active", "is_acknowledged", "is_active"
        ),
        Index("ix_threat_alerts_created_at_severity", "created_at", "severity"),
        CheckConstraint(
            "severity IN ('low', 'medium', 'high', 'critical')",
            name="ck_threat_alerts_severity_valid",
        ),
        CheckConstraint(
            "resolution_status IN ('open', 'investigating', 'resolved', 'closed', 'false_positive')",
            name="ck_threat_alerts_resolution_status_valid",
        ),
        CheckConstraint(
            "length(title) > 0",
            name="ck_threat_alerts_title_not_empty",
        ),
        CheckConstraint(
            "length(threat_type) > 0",
            name="ck_threat_alerts_threat_type_not_empty",
        ),
    )

    id: orm.Mapped[int] = orm.mapped_column(Integer, primary_key=True, index=True)
    title: orm.Mapped[str] = orm.mapped_column(String(500), nullable=False)
    description: orm.Mapped[str | None] = orm.mapped_column(Text, nullable=True)
    severity: orm.Mapped[str] = orm.mapped_column(
        String(50), default="medium", nullable=False
    )
    threat_type: orm.Mapped[str] = orm.mapped_column(String(100), nullable=False)
    source: orm.Mapped[str] = orm.mapped_column(
        String(100), default="system", nullable=False
    )
    affected_users: orm.Mapped[str] = orm.mapped_column(
        Text, default="[]", nullable=False
    )  # JSON string
    affected_ips: orm.Mapped[str] = orm.mapped_column(
        Text, default="[]", nullable=False
    )  # JSON string
    affected_domains: orm.Mapped[str] = orm.mapped_column(
        Text, default="[]", nullable=False
    )  # JSON string
    is_active: orm.Mapped[bool] = orm.mapped_column(
        Boolean, default=True, nullable=False
    )
    is_acknowledged: orm.Mapped[bool] = orm.mapped_column(
        Boolean, default=False, nullable=False
    )
    acknowledged_by: orm.Mapped[str | None] = orm.mapped_column(
        String(255), nullable=True
    )
    acknowledged_at: orm.Mapped[datetime | None] = orm.mapped_column(
        DateTime(timezone=True), nullable=True
    )
    resolution_status: orm.Mapped[str] = orm.mapped_column(
        String(50), default="open", nullable=False
    )
    resolution_notes: orm.Mapped[str | None] = orm.mapped_column(Text, nullable=True)
    resolved_by: orm.Mapped[str | None] = orm.mapped_column(String(255), nullable=True)
    resolved_at: orm.Mapped[datetime | None] = orm.mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: orm.Mapped[datetime] = orm.mapped_column(
        DateTime(timezone=True), default=utils.now, nullable=False
    )
    updated_at: orm.Mapped[datetime] = orm.mapped_column(
        DateTime(timezone=True), default=utils.now, onupdate=utils.now, nullable=False
    )

    @property
    def affected_users_list(self) -> List[int]:
        """Get affected users as a list"""
        try:
            return json.loads(self.affected_users)
        except (json.JSONDecodeError, TypeError):
            return []

    @affected_users_list.setter
    def affected_users_list(self, value: List[int]):
        """Set affected users from a list"""
        self.affected_users = json.dumps(value).decode()

    @property
    def affected_ips_list(self) -> List[str]:
        """Get affected IPs as a list"""
        try:
            return json.loads(self.affected_ips)
        except (json.JSONDecodeError, TypeError):
            return []

    @affected_ips_list.setter
    def affected_ips_list(self, value: List[str]):
        """Set affected IPs from a list"""
        self.affected_ips = json.dumps(value).decode()

    @property
    def affected_domains_list(self) -> List[str]:
        """Get affected domains as a list"""
        try:
            return json.loads(self.affected_domains)
        except (json.JSONDecodeError, TypeError):
            return []

    @affected_domains_list.setter
    def affected_domains_list(self, value: List[str]):
        """Set affected domains from a list"""
        self.affected_domains = json.dumps(value).decode()

