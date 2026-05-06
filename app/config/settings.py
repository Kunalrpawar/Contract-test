"""
Application Configuration Settings
Handles all environment-based configuration using Pydantic Settings
"""

from pydantic_settings import BaseSettings
import logging


class Settings(BaseSettings):
    """Application Settings - loads from .env file"""
    
    # Database
    database_url: str = "sqlite:///./contractiq.db"  # SQLite for local development
    use_sqlite: bool = True  # Use SQLite by default
    
    # Gemini API
    gemini_api_key: str = ""
    
    # JWT
    secret_key: str = "dev-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # File Upload
    max_upload_size: int = 52428800  # 50MB
    allowed_extensions: str = "pdf,docx"
    upload_directory: str = "./uploads"
    
    # Environment
    environment: str = "development"
    log_level: str = "INFO"
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Load settings
settings = Settings()

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
