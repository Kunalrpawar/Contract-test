"""
Database Configuration and Session Management
SQLAlchemy setup for PostgreSQL connection
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# Create database engine
if settings.use_sqlite:
    # SQLite configuration (no connection pooling needed)
    sqlite_url = "sqlite:///./contractiq.db"
    engine = create_engine(
        sqlite_url,
        echo=(settings.environment == "development"),
        connect_args={"check_same_thread": False}
    )
else:
    # PostgreSQL configuration with connection pooling
    engine = create_engine(
        settings.database_url,
        echo=(settings.environment == "development"),
        pool_pre_ping=True,
        pool_size=20,
        max_overflow=40
    )

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db() -> Session:
    """
    Dependency function to get database session
    Usage: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database - create all tables"""
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialized successfully")


def drop_all_tables():
    """Drop all tables - use with caution!"""
    Base.metadata.drop_all(bind=engine)
    logger.warning("All database tables dropped")
