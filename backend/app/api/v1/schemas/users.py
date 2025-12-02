from typing import List, Optional

from pydantic import BaseModel, EmailStr, SecretStr


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
