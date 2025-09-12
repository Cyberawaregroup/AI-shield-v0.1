from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
import json

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=True)
    name = Column(String, nullable=False)
    role = Column(String, default="user")
    hashed_password = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Vulnerability assessment
    age = Column(Integer, nullable=True)
    is_vulnerable = Column(Boolean, default=False)
    vulnerability_factors = Column(Text, default="[]")  # JSON string
    vulnerability_score = Column(Float, default=0.0)
    
    # Security metrics
    risk_score = Column(Float, default=0.0)
    total_breaches = Column(Integer, default=0)
    total_phishing_attempts = Column(Integer, default=0)
    
    # Timestamps
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

# Pydantic models for API requests/responses
class UserCreate(BaseModel):
    email: EmailStr
    phone: Optional[str] = None
    name: str
    role: str = "user"
    age: Optional[int] = None
    vulnerability_factors: Optional[List[str]] = []

class UserUpdate(BaseModel):
    phone: Optional[str] = None
    name: Optional[str] = None
    role: Optional[str] = None
    age: Optional[int] = None
    vulnerability_factors: Optional[List[str]] = None
    risk_score: Optional[float] = None
    total_breaches: Optional[int] = None
    total_phishing_attempts: Optional[int] = None
