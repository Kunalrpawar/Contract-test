"""
Main FastAPI Application
Entry point for ContractIQ service
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import init_db
from app.routes import (
    contracts_router,
    analysis_router,
    validation_router,
    comparison_router,
    health_router,
    frontend_router
)

logger = logging.getLogger(__name__)


# Startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown events"""
    # Startup
    logger.info("Starting ContractIQ API Server...")
    init_db()
    logger.info("Database initialized")
    yield
    # Shutdown
    logger.info("Shutting down ContractIQ API Server...")


# Create FastAPI application
app = FastAPI(
    title="ContractIQ",
    description="AI-Powered Contract Testing & Validation Platform",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_router)
app.include_router(frontend_router)
app.include_router(contracts_router)
app.include_router(analysis_router)
app.include_router(validation_router)
app.include_router(comparison_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=(settings.environment == "development")
    )
