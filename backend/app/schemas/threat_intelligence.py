from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


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
