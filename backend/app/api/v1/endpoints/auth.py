from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone
from jose import jwt
from app.core.database import get_session
from app.core.config import settings
from app.core.security import verify_password, get_password_hash, get_current_user
from app.models.users import User
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    email: str

class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str

def create_access_token(data: dict, expires_delta: timedelta = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

@router.post("/login", response_model=LoginResponse)
async def login(login_data: LoginRequest, db: Session = Depends(get_session)):
    """Login endpoint for demo purposes"""
    try:
        # For demo purposes, accept demo credentials
        if login_data.email == "demo@example.com" and login_data.password == "demo123":
            # Check if demo user exists, create if not
            user = db.query(User).filter(User.email == login_data.email).first()
            if not user:
                user = User(
                    email=login_data.email,
                    name="Demo User",
                    role="user",
                    age=25,
                    vulnerability_factors_list=[]
                )
                user.hashed_password = get_password_hash(login_data.password)
                db.add(user)
                db.commit()
                db.refresh(user)
            
            # Create access token
            access_token = create_access_token(
                data={"sub": str(user.id), "email": user.email}
            )
            
            return LoginResponse(
                access_token=access_token,
                user_id=user.id,
                email=user.email
            )
        else:
            # Check for real user
            user = db.query(User).filter(User.email == login_data.email).first()
            if not user or not verify_password(login_data.password, user.hashed_password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect email or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            # Create access token
            access_token = create_access_token(
                data={"sub": str(user.id), "email": user.email}
            )
            
            return LoginResponse(
                access_token=access_token,
                user_id=user.id,
                email=user.email
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )

@router.post("/register", response_model=LoginResponse)
async def register(register_data: RegisterRequest, db: Session = Depends(get_session)):
    """Register endpoint"""
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == register_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )
        
        # Create new user
        user = User(
            email=register_data.email,
            name=register_data.name,
            role="user",
            age=25,  # Default age
            vulnerability_factors_list=[]
        )
        user.hashed_password = get_password_hash(register_data.password)
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Create access token
        access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email}
        )
        
        return LoginResponse(
            access_token=access_token,
            user_id=user.id,
            email=user.email
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )

@router.get("/me")
async def get_current_user_info(current_user = Depends(get_current_user)):
    """Get current user information"""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name,
        "role": current_user.role
    }
