import logging

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.db import get_session
from app.db.threat_intelligence import BreachExposure, IOC, ThreatAlert
from app.api.v1.schemas.threat_intelligence import (
    IOCCreate,
    IOCResponse,
    ThreatAlertCreate,
    ThreatAlertResponse,
)
from app.services.abuseipdb import AbuseIPDBService
from app.services.hibp import HIBPService
from app.services.phishscan import PhishScanService
from app.services.threat_intelligence import ThreatIntelligenceService
from app.api.v1.schemas.threat_intelligence import PhishingCheckRequest
from app.clients.hibp import HIBPAsyncClient
from app.core.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()


# Service dependencies
async def get_hibp_service():
    # Use async context manager to ensure proper cleanup
    if settings.HIBP_API_KEY:
        async with HIBPAsyncClient(
            api_key=settings.HIBP_API_KEY,
            user_agent="AI-Shield-V1",
            timeout=30.0,
        ) as client:
            yield HIBPService(client=client)
    else:
        yield HIBPService(client=None)


def get_abuseipdb_service():
    return AbuseIPDBService()


def get_phishscan_service():
    return PhishScanService()


def get_threat_intelligence_service(
    hibp_service: HIBPService = Depends(get_hibp_service),
    abuseipdb_service: AbuseIPDBService = Depends(get_abuseipdb_service),
    phishscan_service: PhishScanService = Depends(get_phishscan_service),
):
    return ThreatIntelligenceService(
        hibp_service=hibp_service,
        abuseipdb_service=abuseipdb_service,
        phishscan_service=phishscan_service,
    )


@router.get("/breach-check/{email}")
async def check_email_breaches(
    email: str,
    hibp_service: HIBPService = Depends(get_hibp_service),
    db: Session = Depends(get_session),
):
    """Check if an email has been involved in data breaches"""
    try:
        # Check HIBP for breaches
        breaches = await hibp_service.check_email(email)

        if not breaches:
            return []

        # Return the breaches in our format without storing in database for now
        return [
            {
                "id": i + 1,
                "breach_name": breach.get("Name", "Unknown"),
                "breach_date": breach.get("BreachDate", "2023-01-01"),
                "breach_description": breach.get("Description", ""),
                "data_classes": breach.get("DataClasses", []),
                "severity": "high" if breach.get("PwnCount", 0) > 1000000 else "medium",
                "source": "hibp",
                "source_id": breach.get("Name", ""),
                "created_at": "2023-01-01T00:00:00Z",
            }
            for i, breach in enumerate(breaches)
        ]

    except Exception as e:
        logger.error(f"Error checking breaches for {email}: {e}")
        raise HTTPException(status_code=500, detail="Failed to check email breaches")


@router.get("/ip-check/{ip_address}")
async def check_ip_reputation(
    ip_address: str,
    abuseipdb_service: AbuseIPDBService = Depends(get_abuseipdb_service),
    db: Session = Depends(get_session),
):
    """Check IP address reputation"""
    try:
        # Check AbuseIPDB for IP reputation
        reputation = await abuseipdb_service.check_ip(ip_address)

        # Return the reputation data without storing in database for now
        return reputation

    except Exception as e:
        logger.error(f"Error checking IP reputation for {ip_address}: {e}")
        raise HTTPException(status_code=500, detail="Failed to check IP reputation")


@router.post("/phishing-check")
async def check_phishing_url(
    request: PhishingCheckRequest,
    phishscan_service: PhishScanService = Depends(get_phishscan_service),
    db: Session = Depends(get_session),
):
    """Check if a URL is phishing"""
    try:
        # Check PhishScan for phishing
        result = await phishscan_service.check_url(request.url)

        # Return the result data without storing in database for now
        return result

    except Exception as e:
        logger.error(f"Error checking phishing URL {request.url}: {e}")
        raise HTTPException(status_code=500, detail="Failed to check phishing URL")


@router.get("/stats")
async def get_threat_stats(db: Session = Depends(get_session)):
    """Get threat intelligence statistics"""
    try:
        # Try to get real stats from database
        total_iocs = db.query(IOC).count()
        total_alerts = db.query(ThreatAlert).count()
        total_breaches = db.query(BreachExposure).count()

        recent_alerts = (
            db.query(ThreatAlert).order_by(ThreatAlert.created_at.desc()).limit(5).all()
        )

        return {
            "total_iocs": total_iocs,
            "total_alerts": total_alerts,
            "total_breaches": total_breaches,
            "recent_alerts": [
                {
                    "id": alert.id,
                    "title": alert.title,
                    "severity": alert.severity,
                    "created_at": alert.created_at.isoformat(),
                }
                for alert in recent_alerts
            ],
        }

    except Exception as e:
        logger.error(f"Error fetching threat stats: {e}")
        # Return fallback data
        return {
            "total_iocs": 0,
            "total_alerts": 0,
            "total_breaches": 0,
            "recent_alerts": [],
        }


@router.get("/iocs")
async def get_iocs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_session),
):
    """Get indicators of compromise"""
    try:
        iocs = db.query(IOC).offset(skip).limit(limit).all()
        return [
            {
                "id": ioc.id,
                "value": ioc.value,
                "type": ioc.type,
                "threat_name": ioc.threat_name,
                "description": ioc.description,
                "severity": ioc.severity,
                "confidence_score": ioc.confidence_score,
                "tags": ioc.tags_list,
                "threat_categories": ioc.threat_categories_list,
                "source": ioc.source,
                "first_seen": ioc.first_seen.isoformat(),
                "last_seen": ioc.last_seen.isoformat(),
                "sighting_count": ioc.sighting_count,
                "created_at": ioc.created_at.isoformat(),
            }
            for ioc in iocs
        ]

    except Exception as e:
        logger.error(f"Error fetching IOCs: {e}")
        return []


@router.get("/alerts")
async def get_threat_alerts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_session),
):
    """Get threat alerts"""
    try:
        alerts = db.query(ThreatAlert).offset(skip).limit(limit).all()
        return [
            {
                "id": alert.id,
                "title": alert.title,
                "description": alert.description,
                "severity": alert.severity,
                "threat_type": alert.threat_type,
                "source": alert.source,
                "affected_users": alert.affected_users_list,
                "affected_ips": alert.affected_ips_list,
                "affected_domains": alert.affected_domains_list,
                "is_active": alert.is_active,
                "is_acknowledged": alert.is_acknowledged,
                "resolution_status": alert.resolution_status,
                "created_at": alert.created_at.isoformat(),
            }
            for alert in alerts
        ]

    except Exception as e:
        logger.error(f"Error fetching threat alerts: {e}")
        return []


@router.post("/iocs", response_model=IOCResponse)
async def create_ioc(ioc: IOCCreate, db: Session = Depends(get_session)):
    """Create a new IOC"""
    try:
        db_ioc = IOC(
            value=ioc.value,
            type=ioc.type,
            threat_name=ioc.threat_name,
            description=ioc.description,
            severity=ioc.severity,
            confidence_score=ioc.confidence_score,
            tags_list=ioc.tags or [],
            threat_categories_list=ioc.threat_categories or [],
            source=ioc.source,
        )
        db.add(db_ioc)
        db.commit()
        db.refresh(db_ioc)

        return IOCResponse(
            id=db_ioc.id,
            value=db_ioc.value,
            type=db_ioc.type,
            threat_name=db_ioc.threat_name,
            description=db_ioc.description,
            severity=db_ioc.severity,
            confidence_score=db_ioc.confidence_score,
            tags=db_ioc.tags_list,
            threat_categories=db_ioc.threat_categories_list,
            source=db_ioc.source,
            first_seen=db_ioc.first_seen,
            last_seen=db_ioc.last_seen,
            sighting_count=db_ioc.sighting_count,
            created_at=db_ioc.created_at,
        )

    except Exception as e:
        logger.error(f"Error creating IOC: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create IOC")


@router.post("/alerts", response_model=ThreatAlertResponse)
async def create_threat_alert(
    alert: ThreatAlertCreate, db: Session = Depends(get_session)
):
    """Create a new threat alert"""
    try:
        db_alert = ThreatAlert(
            title=alert.title,
            description=alert.description,
            severity=alert.severity,
            threat_type=alert.threat_type,
            source=alert.source,
            affected_users_list=alert.affected_users or [],
            affected_ips_list=alert.affected_ips or [],
            affected_domains_list=alert.affected_domains or [],
        )
        db.add(db_alert)
        db.commit()
        db.refresh(db_alert)

        return ThreatAlertResponse(
            id=db_alert.id,
            title=db_alert.title,
            description=db_alert.description,
            severity=db_alert.severity,
            threat_type=db_alert.threat_type,
            source=db_alert.source,
            affected_users=db_alert.affected_users_list,
            affected_ips=db_alert.affected_ips_list,
            affected_domains=db_alert.affected_domains_list,
            is_active=db_alert.is_active,
            is_acknowledged=db_alert.is_acknowledged,
            resolution_status=db_alert.resolution_status,
            created_at=db_alert.created_at,
        )

    except Exception as e:
        logger.error(f"Error creating threat alert: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create threat alert")
