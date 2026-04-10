from __future__ import annotations

import os
from dotenv import load_dotenv
from pydantic import BaseSettings, Field, AnyHttpUrl


# Load environment variables in the following order:
# 1) .env (common defaults)
# 2) .env.<ENVIRONMENT> (environment-specific overrides)
ENVIRONMENT = os.getenv("ENVIRONMENT", "development").lower()
load_dotenv(".env", override=False)
load_dotenv(f".env.{ENVIRONMENT}", override=True)


class Settings(BaseSettings):
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

    # App
    PROJECT_NAME: str = Field("PolicyLens", env="PROJECT_NAME")
    API_PREFIX: str = Field("/api", env="API_PREFIX")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
