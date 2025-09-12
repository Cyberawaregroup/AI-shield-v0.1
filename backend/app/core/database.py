from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import OperationalError
from app.core.config import settings
from app.models import users, threat_intelligence, chatbot
import logging

logger = logging.getLogger(__name__)

# Determine database URL based on environment
if settings.ENVIRONMENT == "test":
    DATABASE_URL = "sqlite:///./test.db"
elif settings.ENVIRONMENT == "development":
    # Try PostgreSQL first, fallback to SQLite
    try:
        # Test PostgreSQL connection
        test_engine = create_engine(settings.DATABASE_URL)
        with test_engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        DATABASE_URL = settings.DATABASE_URL
        logger.info("Using PostgreSQL database")
    except Exception as e:
        logger.warning(f"PostgreSQL connection failed: {e}. Falling back to SQLite.")
        DATABASE_URL = "sqlite:///./threat_intel.db"
else:
    DATABASE_URL = settings.DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_recycle=300,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_db_and_tables():
    """Create all database tables"""
    try:
        # Import all models to ensure they're registered
        from app.models.users import User
        from app.models.threat_intelligence import BreachExposure, IOC, ThreatFeed, ThreatAlert
        from app.models.chatbot import ChatSession, ChatMessage, FraudReport, SecurityAdvisor
        
        # Create a single metadata that includes all models
        from sqlalchemy import MetaData
        metadata = MetaData()
        
        # Reflect all tables from all bases
        for base in [users.Base, threat_intelligence.Base, chatbot.Base]:
            for table in base.metadata.tables.values():
                table.tometadata(metadata)
        
        # Create all tables at once
        metadata.create_all(bind=engine)
        
        logger.info("Database tables created successfully")
        
        # Initialize with sample data if tables are empty
        init_sample_data()
        
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise

def init_sample_data():
    """Initialize database with sample data"""
    try:
        db = SessionLocal()
        
        # Check if we already have data
        from app.models.threat_intelligence import ThreatAlert, IOC
        from app.models.users import User
        
        # Create sample threat alerts if none exist
        if db.query(ThreatAlert).count() == 0:
            sample_alerts = [
                ThreatAlert(
                    title="Suspicious Login Attempt",
                    description="Multiple failed login attempts detected from unknown IP",
                    severity="medium",
                    threat_type="authentication",
                    source="system_monitoring",
                    is_active=True
                ),
                ThreatAlert(
                    title="Phishing Email Detected",
                    description="Suspicious email with malicious attachment blocked",
                    severity="high",
                    threat_type="phishing",
                    source="email_gateway",
                    is_active=True
                ),
                ThreatAlert(
                    title="Data Exfiltration Attempt",
                    description="Unusual data transfer pattern detected",
                    severity="critical",
                    threat_type="data_theft",
                    source="network_monitoring",
                    is_active=True
                )
            ]
            db.add_all(sample_alerts)
            
        # Create sample IOCs if none exist
        if db.query(IOC).count() == 0:
            sample_iocs = [
                IOC(
                    value="192.168.1.100",
                    type="ip_address",
                    threat_name="Malicious IP",
                    description="IP address associated with botnet activity",
                    severity="high",
                    confidence_score=0.85,
                    source="threat_feed"
                ),
                IOC(
                    value="malicious-domain.com",
                    type="domain",
                    threat_name="Phishing Domain",
                    description="Domain used in phishing campaigns",
                    severity="high",
                    confidence_score=0.90,
                    source="phish_tank"
                )
            ]
            db.add_all(sample_iocs)
            
        db.commit()
        logger.info("Sample data initialized successfully")
        
    except Exception as e:
        logger.error(f"Error initializing sample data: {e}")
        db.rollback()
    finally:
        db.close()

def get_session() -> Session:
    """Get database session"""
    session = SessionLocal()
    try:
        yield session
    except Exception as e:
        logger.error(f"Database session error: {e}")
        session.rollback()
        raise
    finally:
        session.close()

def init_db():
    """Initialize database with tables and sample data"""
    create_db_and_tables()
