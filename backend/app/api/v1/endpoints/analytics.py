from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from app.core.database import get_session
from app.models.threat_intelligence import BreachExposure, IOC, ThreatAlert
from app.models.users import User
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/dashboard")
async def get_dashboard_analytics(db: Session = Depends(get_session)):
    """Get dashboard analytics overview"""
    try:
        # Get counts
        total_users = db.query(User).count()
        total_breaches = db.query(BreachExposure).count()
        total_iocs = db.query(IOC).count()
        total_alerts = db.query(ThreatAlert).count()
        
        # Get recent activity (last 7 days)
        week_ago = datetime.utcnow() - timedelta(days=7)
        recent_breaches = db.query(BreachExposure).filter(
            BreachExposure.created_at >= week_ago
        ).count()
        
        recent_alerts = db.query(ThreatAlert).filter(
            ThreatAlert.created_at >= week_ago
        ).count()
        
        # Get severity distribution
        high_severity_alerts = db.query(ThreatAlert).filter(
            ThreatAlert.severity == "high"
        ).count()
        
        medium_severity_alerts = db.query(ThreatAlert).filter(
            ThreatAlert.severity == "medium"
        ).count()
        
        low_severity_alerts = db.query(ThreatAlert).filter(
            ThreatAlert.severity == "low"
        ).count()
        
        return {
            "overview": {
                "total_users": total_users,
                "total_breaches": total_breaches,
                "total_iocs": total_iocs,
                "total_alerts": total_alerts
            },
            "recent_activity": {
                "breaches_last_7_days": recent_breaches,
                "alerts_last_7_days": recent_alerts
            },
            "severity_distribution": {
                "high": high_severity_alerts,
                "medium": medium_severity_alerts,
                "low": low_severity_alerts
            }
        }
        
    except Exception as e:
        logger.error(f"Error fetching dashboard analytics: {e}")
        return {
            "overview": {"total_users": 0, "total_breaches": 0, "total_iocs": 0, "total_alerts": 0},
            "recent_activity": {"breaches_last_7_days": 0, "alerts_last_7_days": 0},
            "severity_distribution": {"high": 0, "medium": 0, "low": 0}
        }

@router.get("/breaches/trends")
async def get_breach_trends(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_session)
):
    """Get breach trends over time"""
    try:
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Get breaches by date
        breaches = db.query(BreachExposure).filter(
            BreachExposure.created_at >= start_date
        ).all()
        
        # Group by date
        trends = {}
        for breach in breaches:
            date_str = breach.created_at.strftime("%Y-%m-%d")
            if date_str not in trends:
                trends[date_str] = 0
            trends[date_str] += 1
        
        return {
            "period_days": days,
            "total_breaches": len(breaches),
            "daily_trends": trends
        }
        
    except Exception as e:
        logger.error(f"Error fetching breach trends: {e}")
        return {"period_days": days, "total_breaches": 0, "daily_trends": {}}

@router.get("/iocs/statistics")
async def get_ioc_statistics(db: Session = Depends(get_session)):
    """Get IOC statistics and distribution"""
    try:
        # Get IOCs by type
        ioc_types = db.query(IOC.type).distinct().all()
        type_distribution = {}
        
        for ioc_type in ioc_types:
            count = db.query(IOC).filter(IOC.type == ioc_type[0]).count()
            type_distribution[ioc_type[0]] = count
        
        # Get IOCs by severity
        severity_distribution = {}
        for severity in ["high", "medium", "low"]:
            count = db.query(IOC).filter(IOC.severity == severity).count()
            severity_distribution[severity] = count
        
        # Get top sources
        sources = db.query(IOC.source).distinct().all()
        source_distribution = {}
        
        for source in sources:
            count = db.query(IOC).filter(IOC.source == source[0]).count()
            source_distribution[source[0]] = count
        
        return {
            "total_iocs": db.query(IOC).count(),
            "type_distribution": type_distribution,
            "severity_distribution": severity_distribution,
            "source_distribution": source_distribution
        }
        
    except Exception as e:
        logger.error(f"Error fetching IOC statistics: {e}")
        return {
            "total_iocs": 0,
            "type_distribution": {},
            "severity_distribution": {},
            "source_distribution": {}
        }

@router.get("/users/risk-assessment")
async def get_user_risk_assessment(db: Session = Depends(get_session)):
    """Get user risk assessment analytics"""
    try:
        # Get users by risk level
        high_risk_users = db.query(User).filter(User.risk_score >= 70).count()
        medium_risk_users = db.query(User).filter(
            User.risk_score >= 30, User.risk_score < 70
        ).count()
        low_risk_users = db.query(User).filter(User.risk_score < 30).count()
        
        # Get vulnerable users
        vulnerable_users = db.query(User).filter(User.is_vulnerable == True).count()
        
        # Get average risk score
        avg_risk_score = db.query(User.risk_score).filter(User.risk_score > 0).all()
        if avg_risk_score:
            avg_score = sum(score[0] for score in avg_risk_score) / len(avg_risk_score)
        else:
            avg_score = 0
        
        return {
            "risk_distribution": {
                "high": high_risk_users,
                "medium": medium_risk_users,
                "low": low_risk_users
            },
            "vulnerable_users": vulnerable_users,
            "average_risk_score": round(avg_score, 2),
            "total_users_assessed": db.query(User).filter(User.risk_score > 0).count()
        }
        
    except Exception as e:
        logger.error(f"Error fetching user risk assessment: {e}")
        return {
            "risk_distribution": {"high": 0, "medium": 0, "low": 0},
            "vulnerable_users": 0,
            "average_risk_score": 0,
            "total_users_assessed": 0
        }
