"""
Application configuration management using Pydantic settings.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # Database Configuration
    DATABASE_URL: str = "postgresql://factcheck:password@localhost:5432/factcheck"

    # Redis Configuration
    REDIS_URL: str = "redis://localhost:6379/0"

    # Celery Configuration
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/1"

    # Ollama Configuration
    OLLAMA_API_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama2"

    # Security Configuration
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    API_KEY_SALT: str = "dev-salt-change-in-production"

    # Rate Limiting Configuration
    RATE_LIMIT_FREE_TIER: int = 100
    RATE_LIMIT_PRO_TIER: int = 1000
    RATE_LIMIT_ENTERPRISE_TIER: int = 10000

    # Application Configuration
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    DEBUG: bool = True

    # CORS Configuration
    CORS_ORIGINS: str = "http://localhost:3000"

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    # News Ingestion Configuration
    RSS_FETCH_INTERVAL_MINUTES: int = 30
    ARTICLE_EXTRACTION_TIMEOUT_SECONDS: int = 30
    MAX_ARTICLE_AGE_DAYS: int = 90

    # Vector Search Configuration
    FAISS_INDEX_PATH: str = "./faiss_index"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    EMBEDDING_DIMENSION: int = 384

    # PII Detection Configuration
    PII_DETECTION_ENABLED: bool = True
    PII_DETECTION_CONFIDENCE_THRESHOLD: float = 0.7


# Global settings instance
settings = Settings()
