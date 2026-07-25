"""
Configuration module for Selenium automation framework
"""

import os
from dataclasses import dataclass
from typing import Optional
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass



@dataclass
class Config:
    """Configuration class for Selenium tests"""
    
    # Base URL - MUST be set from environment
    BASE_URL: str = os.getenv("BASE_URL", "http://localhost:5173")
    
    # Browser Configuration
    BROWSER: str = os.getenv("BROWSER", "chrome")
    HEADLESS: bool = os.getenv("HEADLESS", "true").lower() == "true"
    
    # WebDriver Configuration
    IMPLICIT_WAIT: int = int(os.getenv("IMPLICIT_WAIT", "10"))
    EXPLICIT_WAIT: int = int(os.getenv("EXPLICIT_WAIT", "30"))
    PAGE_LOAD_TIMEOUT: int = int(os.getenv("PAGE_LOAD_TIMEOUT", "60"))
    
    # Test Configuration
    RETRY_COUNT: int = int(os.getenv("RETRY_COUNT", "3"))
    RETRY_DELAY: int = int(os.getenv("RETRY_DELAY", "2"))
    
    # Parallel Execution
    PARALLEL_EXECUTION: bool = os.getenv("PARALLEL_EXECUTION", "true").lower() == "true"
    WORKERS: int = int(os.getenv("WORKERS", "4"))
    
    # Reporting
    REPORTS_DIR: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports")
    SCREENSHOTS_DIR: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "screenshots")
    LOGS_DIR: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
    
    # Screenshot Configuration
    SCREENSHOT_ON_FAILURE: bool = True
    SCREENSHOT_ON_SUCCESS: bool = False
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_TO_FILE: bool = True
    LOG_TO_CONSOLE: bool = True
    
    # Test Data
    TEST_DATA_DIR: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    
    # Pass/Fail Threshold
    MIN_PASS_PERCENTAGE: float = float(os.getenv("MIN_PASS_PERCENTAGE", "90.0"))
    MAX_CRITICAL_FAILURES: int = int(os.getenv("MAX_CRITICAL_FAILURES", "20"))
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "production")
    
    @classmethod
    def validate(cls) -> bool:
        """Validate configuration"""
        if not cls.BASE_URL:
            print("Warning: BASE_URL not set, using default")
            return True
        
        # Only validate localhost restriction in CI/CD environment
        if cls.ENVIRONMENT == "production":
            if cls.BASE_URL.startswith("localhost") or cls.BASE_URL.startswith("127.0.0.1"):
                print("Warning: Using localhost in production environment")
        
        return True


# Global configuration instance
config = Config()

# Validate on import (non-blocking for local development)
try:
    config.validate()
except ValueError as e:
    print(f"Configuration Error: {e}")
    # Don't raise for local development flexibility
