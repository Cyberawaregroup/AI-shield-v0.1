from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, SecretStr


# Pydantic models for API requests/responses
class UserCreate(BaseModel):
    email: EmailStr
    phone: Optional[str] = None
    name: str
    role: str = "user"
    age: Optional[int] = None
    vulnerability_factors: Optional[List[str]] = []
    password: SecretStr


class UserUpdate(BaseModel):
    phone: Optional[str] = None
    name: Optional[str] = None
    role: Optional[str] = None
    age: Optional[int] = None
    vulnerability_factors: Optional[List[str]] = None
    risk_score: Optional[float] = None
    total_breaches: Optional[int] = None
    total_phishing_attempts: Optional[int] = None


class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    role: str
    age: Optional[int] = None
    is_vulnerable: bool
    vulnerability_score: float
    risk_score: float
    total_breaches: int
    total_phishing_attempts: int
    created_at: datetime

    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    users: List[UserResponse]
    total: int


class UserCreateResponse(BaseModel):
    id: int
    email: str
    name: str
    role: str
    message: str


class UserUpdateResponse(BaseModel):
    id: int
    email: str
    name: str
    role: str
    message: str


class UserDeleteResponse(BaseModel):
    message: str


class BreachResponse(BaseModel):
    id: int
    breach_name: str
    breach_date: datetime
    breach_description: Optional[str] = None
    data_classes: List[str] = Field(alias="data_classes_list")
    severity: str
    source: str
    created_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True


class UserBreachesResponse(BaseModel):
    breaches: List[BreachResponse]
    total: int
