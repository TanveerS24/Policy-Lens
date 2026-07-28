"""Application settings and configuration."""

from functools import lru_cache
from pathlib import Path
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ROOT_DIR = BASE_DIR.parent

class Settings(BaseSettings):
    """Application configuration settings."""

    # App
    APP_NAME: str = "DentalSchemes India"
    DEBUG: bool = Field(default=False)
    SECRET_KEY: str = Field(default="dev-secret-key-change-in-production")

    # Database
    DATABASE_URL: str = Field(default="postgresql://postgres:postgres@localhost:5432/dentalschemes")

    # Redis
    REDIS_URL: str = Field(default="redis://localhost:6379/0")

    # JWT
    JWT_SECRET_KEY: str = Field(default="dev-jwt-secret-key-change-in-production")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60)
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=30)

    # CORS
    CORS_ORIGINS: str = Field(default="http://localhost:3000,http://localhost:5173,http://localhost:8000,http://localhost:8081,http://127.0.0.1:8000,http://127.0.0.1:8081,exp://localhost:8081,http://192.168.0.101:8081,http://192.168.0.101:8000,http://192.168.0.101:5173,http://192.168.0.101:3000,exp://192.168.0.101:8081,http://172.31.144.1:8081,http://172.31.144.1:8000,http://172.31.144.1:5173,http://172.31.144.1:3000,exp://172.31.144.1:8081")

    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS_ORIGINS string into list."""
        if isinstance(self.CORS_ORIGINS, str):
            return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
        return self.CORS_ORIGINS
    
    ALLOWED_HOSTS: List[str] = Field(default=["*"])

    # File Upload
    MAX_UPLOAD_SIZE_MB: int = 10
    ALLOWED_FILE_TYPES: List[str] = Field(default=["application/pdf", "image/jpeg", "image/png", "image/tiff"])
    S3_BUCKET: str = Field(default="dentalschemes-docs")
    AWS_ACCESS_KEY_ID: str = Field(default="")
    AWS_SECRET_ACCESS_KEY: str = Field(default="")
    AWS_REGION: str = Field(default="ap-south-1")

    # AI/LLM
    ANTHROPIC_API_KEY: str = Field(default="")
    OPENAI_API_KEY: str = Field(default="")
    AI_TIMEOUT_SECONDS: int = 60

    # SMS/OTP
    SMS_API_KEY: str = Field(default="")
    SMS_PROVIDER: str = Field(default="")
    OTP_EXPIRE_MINUTES: int = Field(default=10)
    OTP_MAX_ATTEMPTS: int = Field(default=3)
    OTP_MAX_REQUESTS_PER_HOUR: int = Field(default=5)

    # SMTP Email
    SMTP_HOST: str = Field(default="")
    SMTP_PORT: int = Field(default=587)
    SMTP_USER: str = Field(default="")
    SMTP_PASSWORD: str = Field(default="")
    EMAILS_FROM_EMAIL: str = Field(default="noreply@dentalschemes.in")
    EMAILS_FROM_NAME: str = Field(default="Policy-Lens Dental Schemes")

    # Security
    MAX_LOGIN_ATTEMPTS: int = Field(default=5)
    LOCKOUT_DURATION_MINUTES: int = Field(default=30)

    model_config = {
        "env_file": (
            str(BASE_DIR / ".env"),
            str(ROOT_DIR / ".env"),
            ".env",
        ),
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
