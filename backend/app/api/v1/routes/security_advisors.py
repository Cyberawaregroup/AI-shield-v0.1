import logging

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.db import get_session
from app.db.chatbot import SecurityAdvisor

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/")
async def get_security_advisors(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_session),
):
    """Get all security advisors"""
    try:
        advisors = db.query(SecurityAdvisor).offset(skip).limit(limit).all()
        return [
            {
                "id": advisor.id,
                "name": advisor.name,
                "email": advisor.email,
                "phone": advisor.phone,
                "specialization": advisor.specialization_list,
                "certifications": advisor.certifications_list,
                "experience_years": advisor.experience_years,
                "is_available": advisor.is_available,
                "current_load": advisor.current_load,
                "max_load": advisor.max_load,
                "available_hours": advisor.available_hours_dict,
                "created_at": advisor.created_at.isoformat(),
            }
            for advisor in advisors
        ]
    except Exception as e:
        logger.error(f"Error fetching security advisors: {e}")
        return []


@router.get("/{advisor_id}")
async def get_security_advisor(advisor_id: int, db: Session = Depends(get_session)):
    """Get a specific security advisor by ID"""
    try:
        advisor = (
            db.query(SecurityAdvisor).filter(SecurityAdvisor.id == advisor_id).first()
        )
        if advisor is None:
            raise HTTPException(status_code=404, detail="Security advisor not found")

        return {
            "id": advisor.id,
            "name": advisor.name,
            "email": advisor.email,
            "phone": advisor.phone,
            "specialization": advisor.specialization_list,
            "certifications": advisor.certifications_list,
            "experience_years": advisor.experience_years,
            "is_available": advisor.is_available,
            "current_load": advisor.current_load,
            "max_load": advisor.max_load,
            "available_hours": advisor.available_hours_dict,
            "created_at": advisor.created_at.isoformat(),
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching security advisor {advisor_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch security advisor")


@router.get("/available")
async def get_available_advisors(db: Session = Depends(get_session)):
    """Get all available security advisors"""
    try:
        advisors = (
            db.query(SecurityAdvisor)
            .filter(SecurityAdvisor.is_available.is_(True))
            .all()
        )
        return [
            {
                "id": advisor.id,
                "name": advisor.name,
                "email": advisor.email,
                "specialization": advisor.specialization_list,
                "experience_years": advisor.experience_years,
                "current_load": advisor.current_load,
                "max_load": advisor.max_load,
            }
            for advisor in advisors
        ]
    except Exception as e:
        logger.error(f"Error fetching available advisors: {e}")
        return []
