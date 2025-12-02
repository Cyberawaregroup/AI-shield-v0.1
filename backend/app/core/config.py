from pathlib import Path
import typing

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Threat Intelligence Platform"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: typing.Literal["development", "staging", "production"] = "development"
    DEBUG: bool = True

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

    # CORS
    ALLOWED_ORIGINS: typing.List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]
    ALLOWED_HOSTS: typing.List[str] = ["localhost", "127.0.0.1"]

    # Database - Use SQLite for local development
    DATABASE_URL: str = "sqlite:///./threat_intel.db"
    ASYNC_DATABASE_URL: str = "sqlite+aiosqlite:///./threat_intel.db"

    # Redis - Optional for local development
    REDIS_URL: str = "redis://localhost:6379/0"

    # External APIs
    HF_TOKEN: typing.Optional[str] = None  # Hugging Face API token for GPT-OSS models
    TWILIO_ACCOUNT_SID: typing.Optional[str] = None
    TWILIO_AUTH_TOKEN: typing.Optional[str] = None

    # Threat Intelligence APIs
    HIBP_API_KEY: typing.Optional[str] = None
    ABUSEIPDB_API_KEY: typing.Optional[str] = None
    SOCRADAR_API_KEY: typing.Optional[str] = None
    NETCRAFT_API_KEY: typing.Optional[str] = None
    ZVELO_API_KEY: typing.Optional[str] = None

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # File Upload
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    UPLOAD_DIR: Path = Path("uploads")

    # Celery - Optional for local development
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"

    # Monitoring
    ENABLE_METRICS: bool = True
    METRICS_PORT: int = 9090

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

# Ensure upload directory exists
settings.UPLOAD_DIR.mkdir(exist_ok=True, mode=0o755)
