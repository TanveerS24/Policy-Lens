"""
Application Settings and Configuration
"""

from typing import List
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # API Configuration
    API_TITLE: str = "Healthcare Policy Intelligence Platform"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "AI-powered healthcare policy understanding and eligibility checking"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Database Configuration
    MONGO_URI: str = "mongodb://localhost:27017/policy_lens"
    MONGO_DB_NAME: str = "policy_lens"
    
    # JWT Configuration
    JWT_SECRET: str = "your-super-secret-jwt-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Redis Configuration
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Ollama Configuration
    OLLAMA_URL: str = "http://localhost:11434"
    OLLAMA_SUMMARIZATION_MODEL: str = "gemma3:4b-it-q4_K_M"
    OLLAMA_REASONING_MODEL: str = "llama3.2:3b-instruct-q4_K_M"
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8081", "*"]
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1"]
    
    # OTP Configuration
    OTP_EXPIRY_MINUTES: int = 10
    OTP_LENGTH: int = 6
    
    # Upload Configuration
    MAX_UPLOAD_SIZE: int = 50000000  # 50MB
    UPLOADS_DIR: str = "./uploads"
    ALLOWED_EXTENSIONS: List[str] = ["pdf"]
    
    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    LOG_DIR: str = "./logs"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


settings = get_settings()
