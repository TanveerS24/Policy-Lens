"""
Logging utilities for Selenium automation
"""

import os
import sys
from datetime import datetime
from loguru import logger
from config.config import config


class TestLogger:
    """Custom logger for test execution"""
    
    def __init__(self):
        self.setup_logger()
    
    def setup_logger(self):
        """Configure loguru logger"""
        # Remove default handler
        logger.remove()
        
        # Console handler
        if config.LOG_TO_CONSOLE:
            logger.add(
                sys.stdout,
                format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
                level=config.LOG_LEVEL,
                colorize=True
            )
        
        # File handler
        if config.LOG_TO_FILE:
            log_file = os.path.join(
                config.LOGS_DIR,
                f"test_execution_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
            )
            logger.add(
                log_file,
                format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
                level=config.LOG_LEVEL,
                rotation="50 MB",
                retention="30 days",
                compression="zip"
            )
        
        # Error file handler
        error_log_file = os.path.join(
            config.LOGS_DIR,
            f"errors_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        )
        logger.add(
            error_log_file,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            level="ERROR",
            rotation="50 MB",
            retention="30 days",
            compression="zip"
        )
    
    def info(self, message: str):
        """Log info message"""
        logger.info(message)
    
    def debug(self, message: str):
        """Log debug message"""
        logger.debug(message)
    
    def warning(self, message: str):
        """Log warning message"""
        logger.warning(message)
    
    def error(self, message: str):
        """Log error message"""
        logger.error(message)
    
    def critical(self, message: str):
        """Log critical message"""
        logger.critical(message)
    
    def test_start(self, test_name: str):
        """Log test start"""
        logger.info(f"{'='*60}")
        logger.info(f"TEST START: {test_name}")
        logger.info(f"{'='*60}")
    
    def test_end(self, test_name: str, status: str, duration: float = 0):
        """Log test end"""
        logger.info(f"{'='*60}")
        logger.info(f"TEST END: {test_name}")
        logger.info(f"Status: {status}")
        logger.info(f"Duration: {duration:.2f}s")
        logger.info(f"{'='*60}")
    
    def step(self, step_number: int, description: str):
        """Log test step"""
        logger.info(f"Step {step_number}: {description}")


# Global logger instance
test_logger = TestLogger()
