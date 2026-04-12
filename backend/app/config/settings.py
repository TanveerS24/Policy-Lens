from __future__ import annotations

import os
from dotenv import load_dotenv
from pydantic import Field, AnyHttpUrl
from pydantic_settings import BaseSettings


# Load environment variables in the following order:
# 1) .env (common defaults)
# 2) .env.<ENVIRONMENT> (environment-specific overrides)
ENVIRONMENT = os.getenv("ENVIRONMENT", "development").lower()
load_dotenv(".env", override=False)
load_dotenv(f".env.{ENVIRONMENT}", override=True)


class Settings(BaseSettings):
    # Environment
    ENVIRONMENT: str = Field("development", env="ENVIRONMENT")

    # Database
    MONGO_URI: str = Field("mongodb://mongodb:27017/policy_lens", env="MONGO_URI")

    # Caching / ephemeral stores
    REDIS_URL: str = Field("redis://redis:6379", env="REDIS_URL")

    # JWT
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    JWT_ALGORITHM: str = Field("HS256", env="JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(15, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(7, env="REFRESH_TOKEN_EXPIRE_DAYS")

    # Ollama / LLM
    OLLAMA_URL: AnyHttpUrl = Field("http://ollama:11434", env="OLLAMA_URL")
    OLLAMA_SUMMARY_MODEL: str = Field("gemma3:4b-it-q4_K_M", env="OLLAMA_SUMMARY_MODEL")
    OLLAMA_QA_MODEL: str = Field("llama3.2:3b-instruct-q4_K_M", env="OLLAMA_QA_MODEL")

    # SMS Gateway (MSG91)
    MSG91_API_KEY: str = Field("", env="MSG91_API_KEY")
    MSG91_SENDER_ID: str = Field("DNTSCM", env="MSG91_SENDER_ID")
    MSG91_TEMPLATE_ID: str = Field("", env="MSG91_TEMPLATE_ID")

    # OTP Configuration
    OTP_TTL_SECONDS: int = Field(600, env="OTP_TTL_SECONDS")  # 10 minutes
    OTP_MAX_ATTEMPTS: int = Field(3, env="OTP_MAX_ATTEMPTS")
    OTP_MAX_REQUESTS_PER_HOUR: int = Field(5, env="OTP_MAX_REQUESTS_PER_HOUR")
    ACCOUNT_LOCKOUT_MINUTES: int = Field(30, env="ACCOUNT_LOCKOUT_MINUTES")
    MAX_LOGIN_ATTEMPTS: int = Field(5, env="MAX_LOGIN_ATTEMPTS")

    # App
    PROJECT_NAME: str = Field("DentalSchemes India", env="PROJECT_NAME")
    API_PREFIX: str = Field("/api/v1", env="API_PREFIX")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
