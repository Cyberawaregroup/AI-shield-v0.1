#!/usr/bin/env python3
"""
Database initialization script
This script ensures the database is properly set up with all required tables
"""

import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

from app.core.database import create_db_and_tables, engine
from app.models.users import User, Base
from sqlalchemy.orm import sessionmaker
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_database():
    """Initialize the database with all required tables"""
    
    print("🗄️ Initializing Database")
    print("=" * 30)
    
    try:
        # Create all tables
        print("Creating database tables...")
        create_db_and_tables()
        print("✅ Database tables created successfully")
        
        # Test database connection
        print("Testing database connection...")
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = SessionLocal()
        
        # Test query
        result = session.execute("SELECT 1").scalar()
        if result == 1:
            print("✅ Database connection successful")
        else:
            print("❌ Database connection test failed")
            return False
        
        session.close()
        
        print("\n🎉 Database initialization complete!")
        print("You can now start the backend server.")
        
        return True
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        print(f"❌ Database initialization failed: {e}")
        return False

if __name__ == "__main__":
    success = init_database()
    sys.exit(0 if success else 1)
