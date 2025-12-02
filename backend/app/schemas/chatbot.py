from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


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
