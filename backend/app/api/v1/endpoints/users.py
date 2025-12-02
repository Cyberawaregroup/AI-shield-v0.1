import logging

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.v1.schemas.users import UserCreate, UserUpdate
from app.core.db import get_session
from app.core.security import get_password_hash
from app.db.threat_intelligence import BreachExposure
from app.db.users import User

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/")
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_session),
):
    """Get all users"""
    try:
        users = db.query(User).offset(skip).limit(limit).all()
        return [
            {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "role": user.role,
                "age": user.age,
                "is_vulnerable": user.is_vulnerable,
                "vulnerability_score": user.vulnerability_score,
                "risk_score": user.risk_score,
                "total_breaches": user.total_breaches,
                "total_phishing_attempts": user.total_phishing_attempts,
                "created_at": user.created_at.isoformat(),
            }
            for user in users
        ]
    except Exception as e:
        logger.error(f"Error fetching users: {e}")
        return []


@router.get("/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_session)):
    """Get a specific user by ID"""
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "role": user.role,
            "age": user.age,
            "is_vulnerable": user.is_vulnerable,
            "vulnerability_score": user.vulnerability_score,
            "risk_score": user.risk_score,
            "total_breaches": user.total_breaches,
            "total_phishing_attempts": user.total_phishing_attempts,
            "created_at": user.created_at.isoformat(),
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch user")


@router.post("/")
async def create_user(user: UserCreate, db: Session = Depends(get_session)):
    """Create a new user"""
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            raise HTTPException(
                status_code=400, detail="User with this email already exists"
            )

        # Create new user
        db_user = User(
            email=user.email,
            name=user.name,
            role=user.role,
            age=user.age,
            vulnerability_factors_list=user.vulnerability_factors or [],
        )
        db_user.hashed_password = get_password_hash(user.password.get_secret_value())

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return {
            "id": db_user.id,
            "email": db_user.email,
            "name": db_user.name,
            "role": db_user.role,
            "message": "User created successfully",
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create user")


@router.put("/{user_id}")
async def update_user(
    user_id: int, user_update: UserUpdate, db: Session = Depends(get_session)
):
    """Update a user"""
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        # Update fields if provided
        if user_update.name is not None:
            db_user.name = user_update.name
        if user_update.role is not None:
            db_user.role = user_update.role
        if user_update.age is not None:
            db_user.age = user_update.age
        if user_update.vulnerability_factors is not None:
            db_user.vulnerability_factors_list = user_update.vulnerability_factors
        if user_update.risk_score is not None:
            db_user.risk_score = user_update.risk_score
        if user_update.total_breaches is not None:
            db_user.total_breaches = user_update.total_breaches
        if user_update.total_phishing_attempts is not None:
            db_user.total_phishing_attempts = user_update.total_phishing_attempts

        db.commit()
        db.refresh(db_user)

        return {
            "id": db_user.id,
            "email": db_user.email,
            "name": db_user.name,
            "role": db_user.role,
            "message": "User updated successfully",
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating user {user_id}: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update user")


@router.delete("/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_session)):
    """Delete a user"""
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        db.delete(db_user)
        db.commit()

        return {"message": "User deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting user {user_id}: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete user")


@router.get("/{user_id}/breaches")
async def get_user_breaches(user_id: int, db: Session = Depends(get_session)):
    """Get breach exposures for a specific user"""
    try:

        breaches = (
            db.query(BreachExposure).filter(BreachExposure.user_id == user_id).all()
        )
        return [
            {
                "id": breach.id,
                "breach_name": breach.breach_name,
                "breach_date": breach.breach_date.isoformat(),
                "breach_description": breach.breach_description,
                "data_classes": breach.data_classes_list,
                "severity": breach.severity,
                "source": breach.source,
                "created_at": breach.created_at.isoformat(),
            }
            for breach in breaches
        ]
    except Exception as e:
        logger.error(f"Error fetching breaches for user {user_id}: {e}")
        return []
