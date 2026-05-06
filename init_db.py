"""
Database initialization script
Run migrations and setup initial data
"""

from app.database import init_db
from app.config import logger

if __name__ == "__main__":
    logger.info("Initializing database...")
    init_db()
    logger.info("Database initialization complete!")
