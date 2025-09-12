from sqlmodel import SQLModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    CITIZEN = "citizen"
    VOLUNTEER = "volunteer"
    ADMIN = "admin"
    IT_DIRECTOR = "it_director"

class VulnerabilityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class User(SQLModel, table=True):
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    phone_number: Optional[str] = Field(default=None, index=True)
    first_name: str
    last_name: str
    role: UserRole = Field(default=UserRole.CITIZEN)
    
    # Vulnerability assessment
    age: Optional[int] = Field(default=None)
    is_vulnerable: bool = Field(default=False)
    vulnerability_factors: List[str] = Field(default_factory=list)  # JSON array
    vulnerability_score: int = Field(default=0, ge=0, le=100)
    
    # Security metrics
    risk_score: int = Field(default=0, ge=0, le=100)
    last_security_check: Optional[datetime] = Field(default=None)
    total_breaches: int = Field(default=0)
    total_phishing_attempts: int = Field(default=0)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = Field(default=None)
    
    # Account status
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "caroline@example.com",
                "phone_number": "+44123456789",
                "first_name": "Caroline",
                "last_name": "Smith",
                "role": "citizen",
                "age": 68,
                "is_vulnerable": True,
                "vulnerability_factors": ["elderly", "recent_stress"],
                "vulnerability_score": 75,
                "risk_score": 30
            }
        }

class UserCreate(SQLModel):
    email: str
    phone_number: Optional[str] = None
    first_name: str
    last_name: str
    age: Optional[int] = None
    vulnerability_factors: List[str] = Field(default_factory=list)

class UserUpdate(SQLModel):
    phone_number: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = None
    vulnerability_factors: Optional[List[str]] = None
    is_vulnerable: Optional[bool] = None

class UserResponse(SQLModel):
    id: int
    email: str
    phone_number: Optional[str] = None
    first_name: str
    last_name: str
    role: UserRole
    age: Optional[int] = None
    is_vulnerable: bool
    vulnerability_score: int
    risk_score: int
    total_breaches: int
    total_phishing_attempts: int
    created_at: datetime
    last_login: Optional[datetime] = None
