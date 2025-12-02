import logging
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.threat_intelligence import (
    IOC,
    IOCResponse,
    IOCCreate,
    ThreatAlert,
    ThreatAlertResponse,
    ThreatAlertCreate,
    BreachExposure,
    ThreatFeed,
)
from app.services.hibp_service import HIBPService
from app.services.abuseipdb_service import AbuseIPDBService
from app.services.phishscan_service import PhishScanService
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


class ThreatIntelligenceService:
    """Service for managing threat intelligence operations"""

    def __init__(
        self,
        hibp_service: HIBPService,
        abuseipdb_service: AbuseIPDBService,
        phishscan_service: PhishScanService,
    ):
        self.hibp_service = hibp_service
        self.abuseipdb_service = abuseipdb_service
        self.phishscan_service = phishscan_service

    async def check_email_breaches(
        self, email: str, db_session: Session
    ) -> List[Dict[str, Any]]:
        """Check if an email has been involved in data breaches"""
        try:
            # Check HIBP for breaches
            breaches = await self.hibp_service.check_email(email)

            # Store breaches in database
            for breach in breaches:
                breach_exposure = BreachExposure(
                    user_id=None,  # Will be set when user is authenticated
                    breach_name=breach.get("Name", "Unknown Breach"),
                    breach_date=breach.get("BreachDate"),
                    breach_description=breach.get("Description"),
                    data_classes=breach.get("DataClasses", []),
                    severity=breach.get("Severity", "medium"),
                    source="hibp",
                    source_id=breach.get("Name"),
                )
                db_session.add(breach_exposure)

            db_session.commit()
            return breaches

        except Exception as e:
            logger.error(f"Error checking breaches for {email}: {str(e)}")
            db_session.rollback()
            return []

    async def check_ip_reputation(
        self, ip_address: str, db_session: Session
    ) -> Dict[str, Any]:
        """Check IP address reputation using AbuseIPDB"""
        try:
            reputation = await self.abuseipdb_service.check_ip(ip_address)

            # Store IOC if malicious
            if reputation.get("abuse_confidence_score", 0) > 50:
                ioc = IOC(
                    value=ip_address,
                    type="ip_address",
                    threat_name="Malicious IP",
                    description=f"IP with {reputation.get('abuse_confidence_score')}% abuse confidence",
                    severity="high"
                    if reputation.get("abuse_confidence_score", 0) > 80
                    else "medium",
                    confidence_score=reputation.get("abuse_confidence_score", 0)
                    / 100.0,
                    source="abuseipdb",
                    source_id=ip_address,
                )
                db_session.add(ioc)
                db_session.commit()

            return reputation

        except Exception as e:
            logger.error(f"Error checking IP reputation for {ip_address}: {str(e)}")
            return {"error": str(e)}

    async def check_phishing_url(self, url: str, db_session: Session) -> Dict[str, Any]:
        """Check if a URL is phishing using zvelo PhishScan"""
        try:
            result = await self.phishscan_service.check_url(url)

            # Store IOC if malicious
            if result.get("is_phishing", False):
                ioc = IOC(
                    value=url,
                    type="url",
                    threat_name="Phishing URL",
                    description="URL identified as phishing by zvelo PhishScan",
                    severity="high",
                    confidence_score=result.get("confidence", 0.8),
                    source="zvelo",
                    source_id=url,
                )
                db_session.add(ioc)
                db_session.commit()

            return result

        except Exception as e:
            logger.error(f"Error checking phishing URL {url}: {str(e)}")
            return {"error": str(e)}

    async def get_iocs(
        self, db_session: Session, limit: int = 100
    ) -> List[IOCResponse]:
        """Get all IOCs from database"""
        try:
            statement = select(IOC).limit(limit)
            iocs = db_session.execute(statement).scalars().all()
            return [
                IOCResponse(
                    id=ioc.id,
                    value=ioc.value,
                    type=ioc.type,
                    threat_name=ioc.threat_name,
                    description=ioc.description,
                    severity=ioc.severity,
                    confidence_score=ioc.confidence_score,
                    tags=ioc.tags_list,
                    threat_categories=ioc.threat_categories_list,
                    source=ioc.source,
                    first_seen=ioc.first_seen,
                    last_seen=ioc.last_seen,
                    sighting_count=ioc.sighting_count,
                    created_at=ioc.created_at,
                )
                for ioc in iocs
            ]
        except Exception as e:
            logger.error(f"Error getting IOCs: {str(e)}")
            return []

    async def create_ioc(
        self, ioc_data: IOCCreate, db_session: Session
    ) -> Optional[IOCResponse]:
        """Create a new IOC"""
        try:
            ioc = IOC(
                value=ioc_data.value,
                type=ioc_data.type,
                threat_name=ioc_data.threat_name,
                description=ioc_data.description,
                severity=ioc_data.severity,
                confidence_score=ioc_data.confidence_score,
                tags=ioc_data.tags,
                threat_categories=ioc_data.threat_categories,
                source=ioc_data.source,
            )
            db_session.add(ioc)
            db_session.commit()
            db_session.refresh(ioc)
            return IOCResponse(
                id=ioc.id,
                value=ioc.value,
                type=ioc.type,
                threat_name=ioc.threat_name,
                description=ioc.description,
                severity=ioc.severity,
                confidence_score=ioc.confidence_score,
                tags=ioc.tags_list,
                threat_categories=ioc.threat_categories_list,
                source=ioc.source,
                first_seen=ioc.first_seen,
                last_seen=ioc.last_seen,
                sighting_count=ioc.sighting_count,
                created_at=ioc.created_at,
            )
        except Exception as e:
            logger.error(f"Error creating IOC: {str(e)}")
            db_session.rollback()
            return None

    async def get_threat_alerts(
        self, db_session: Session, limit: int = 100
    ) -> List[ThreatAlertResponse]:
        """Get all threat alerts from database"""
        try:
            statement = select(ThreatAlert).limit(limit)
            alerts = db_session.execute(statement).scalars().all()
            return [
                ThreatAlertResponse(
                    id=alert.id,
                    title=alert.title,
                    description=alert.description,
                    severity=alert.severity,
                    threat_type=alert.threat_type,
                    source=alert.source,
                    affected_users=alert.affected_users_list,
                    affected_ips=alert.affected_ips_list,
                    affected_domains=alert.affected_domains_list,
                    is_active=alert.is_active,
                    is_acknowledged=alert.is_acknowledged,
                    resolution_status=alert.resolution_status,
                    created_at=alert.created_at,
                )
                for alert in alerts
            ]
        except Exception as e:
            logger.error(f"Error getting threat alerts: {str(e)}")
            return []

    async def create_threat_alert(
        self, alert_data: ThreatAlertCreate, db_session: Session
    ) -> Optional[ThreatAlertResponse]:
        """Create a new threat alert"""
        try:
            alert = ThreatAlert(
                title=alert_data.title,
                description=alert_data.description,
                severity=alert_data.severity,
                threat_type=alert_data.threat_type,
                source=alert_data.source,
                affected_users=alert_data.affected_users,
                affected_ips=alert_data.affected_ips,
                affected_domains=alert_data.affected_domains,
            )
            db_session.add(alert)
            db_session.commit()
            db_session.refresh(alert)
            return ThreatAlertResponse(
                id=alert.id,
                title=alert.title,
                description=alert.description,
                severity=alert.severity,
                threat_type=alert.threat_type,
                source=alert.source,
                affected_users=alert.affected_users_list,
                affected_ips=alert.affected_ips_list,
                affected_domains=alert.affected_domains_list,
                is_active=alert.is_active,
                is_acknowledged=alert.is_acknowledged,
                resolution_status=alert.resolution_status,
                created_at=alert.created_at,
            )
        except Exception as e:
            logger.error(f"Error creating threat alert: {str(e)}")
            db_session.rollback()
            return None

    async def get_threat_feeds(self, db_session: Session) -> List[ThreatFeed]:
        """Get all threat feeds from database"""
        try:
            statement = select(ThreatFeed)
            feeds = db_session.execute(statement).scalars().all()
            return feeds
        except Exception as e:
            logger.error(f"Error getting threat feeds: {str(e)}")
            return []

    async def refresh_threat_feed(self, feed_id: int, db_session: Session) -> bool:
        """Refresh a specific threat feed"""
        try:
            statement = select(ThreatFeed).where(ThreatFeed.id == feed_id)
            feed = db_session.execute(statement).scalar_one_or_none()

            if not feed:
                return False

            # Update feed status
            feed.last_update = datetime.now(timezone.utc)
            db_session.add(feed)
            db_session.commit()

            logger.info(f"Refreshed threat feed: {feed.name}")
            return True

        except Exception as e:
            logger.error(f"Error refreshing threat feed {feed_id}: {str(e)}")
            db_session.rollback()
            return False

    async def get_threat_stats(self, db_session: Session) -> Dict[str, Any]:
        """Get overall threat statistics"""
        try:
            # Count IOCs by type
            ioc_statement = select(IOC)
            iocs = db_session.execute(ioc_statement).scalars().all()

            ioc_counts = {}
            for ioc in iocs:
                ioc_type = ioc.type
                ioc_counts[ioc_type] = ioc_counts.get(ioc_type, 0) + 1

            # Count alerts by severity
            alert_statement = select(ThreatAlert)
            alerts = db_session.execute(alert_statement).scalars().all()

            alert_counts = {}
            for alert in alerts:
                severity = alert.severity
                alert_counts[severity] = alert_counts.get(severity, 0) + 1

            # Count breaches
            breach_statement = select(BreachExposure)
            breaches = db_session.execute(breach_statement).scalars().all()

            return {
                "total_iocs": len(iocs),
                "ioc_counts_by_type": ioc_counts,
                "total_alerts": len(alerts),
                "alert_counts_by_severity": alert_counts,
                "total_breaches": len(breaches),
                "last_updated": datetime.now(timezone.utc).isoformat(),
            }

        except Exception as e:
            logger.error(f"Error getting threat stats: {str(e)}")
            return {"error": str(e)}
