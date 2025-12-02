from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Float,
    DateTime,
    Text,
    ForeignKey,
)
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum
import json

Base = declarative_base()


class BreachExposure(Base):
    __tablename__ = "breach_exposures"

    id = Column(Integer, primary_key=True, index=True)
    breach_name = Column(String, nullable=False)
    breach_date = Column(DateTime, nullable=False)
    breach_description = Column(Text, nullable=True)
    data_classes = Column(Text, default="[]")  # JSON string
    severity = Column(String, default="medium")
    source = Column(String, default="hibp")
    source_id = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

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
        self.data_classes = json.dumps(value)


class IOC(Base):
    __tablename__ = "indicators_of_compromise"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(String, nullable=False, index=True)
    type = Column(String, nullable=False)
    threat_name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    severity = Column(String, default="medium")
    confidence_score = Column(Float, default=0.0)
    tags = Column(Text, default="[]")  # JSON string
    threat_categories = Column(Text, default="[]")  # JSON string
    source = Column(String, default="manual")
    source_id = Column(String, nullable=True)
    first_seen = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow)
    sighting_count = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

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
        self.tags = json.dumps(value)

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
        self.threat_categories = json.dumps(value)


class ThreatFeed(Base):
    __tablename__ = "threat_feeds"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    source_url = Column(String, nullable=True)
    feed_type = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    last_updated = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)


class ThreatAlert(Base):
    __tablename__ = "threat_alerts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    severity = Column(String, default="medium")
    threat_type = Column(String, nullable=False)
    source = Column(String, default="system")
    affected_users = Column(Text, default="[]")  # JSON string
    affected_ips = Column(Text, default="[]")  # JSON string
    affected_domains = Column(Text, default="[]")  # JSON string
    is_active = Column(Boolean, default=True)
    is_acknowledged = Column(Boolean, default=False)
    acknowledged_by = Column(String, nullable=True)
    acknowledged_at = Column(DateTime, nullable=True)
    resolution_status = Column(String, default="open")
    resolution_notes = Column(Text, nullable=True)
    resolved_by = Column(String, nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

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
        self.affected_users = json.dumps(value)

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
        self.affected_ips = json.dumps(value)

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
        self.affected_domains = json.dumps(value)


# Pydantic models for API requests/responses
class IOCCreate(BaseModel):
    value: str
    type: str
    threat_name: str
    description: Optional[str] = None
    severity: str = "medium"
    confidence_score: float = 0.0
    tags: Optional[List[str]] = []
    threat_categories: Optional[List[str]] = []
    source: str = "manual"


class IOCResponse(BaseModel):
    id: int
    value: str
    type: str
    threat_name: str
    description: Optional[str] = None
    severity: str
    confidence_score: float
    tags: List[str]
    threat_categories: List[str]
    source: str
    first_seen: datetime
    last_seen: datetime
    sighting_count: int
    created_at: datetime


class ThreatAlertCreate(BaseModel):
    title: str
    description: Optional[str] = None
    severity: str = "medium"
    threat_type: str
    source: str = "system"
    affected_users: Optional[List[int]] = []
    affected_ips: Optional[List[str]] = []
    affected_domains: Optional[List[str]] = []


class ThreatAlertResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    severity: str
    threat_type: str
    source: str
    affected_users: List[int]
    affected_ips: List[str]
    affected_domains: List[str]
    is_active: bool
    is_acknowledged: bool
    resolution_status: str
    created_at: datetime
