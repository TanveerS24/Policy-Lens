"""
Screenshot capture utilities
"""

import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from config.config import config
from utils.logger import test_logger


class ScreenshotManager:
    """Manager for capturing and storing screenshots"""
    
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.ensure_screenshots_dir()
    
    def ensure_screenshots_dir(self):
        """Ensure screenshots directory exists"""
        os.makedirs(config.SCREENSHOTS_DIR, exist_ok=True)
    
    def capture(self, test_name: str, status: str = "info") -> str:
        """
        Capture screenshot
        
        Args:
            test_name: Name of the test
            status: Status of the test (passed, failed, info)
        
        Returns:
            Path to the captured screenshot
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{test_name}_{status}_{timestamp}.png"
        filepath = os.path.join(config.SCREENSHOTS_DIR, filename)
        
        try:
            self.driver.save_screenshot(filepath)
            test_logger.info(f"Screenshot captured: {filepath}")
            return filepath
        except Exception as e:
            test_logger.error(f"Failed to capture screenshot: {e}")
            return ""
    
    def capture_on_failure(self, test_name: str, error: str = None) -> str:
        """
        Capture screenshot on test failure
        
        Args:
            test_name: Name of the test
            error: Error message if any
        
        Returns:
            Path to the captured screenshot
        """
        if config.SCREENSHOT_ON_FAILURE:
            filepath = self.capture(test_name, "failed")
            if error:
                self._add_error_annotation(filepath, error)
            return filepath
        return ""
    
    def capture_on_success(self, test_name: str) -> str:
        """
        Capture screenshot on test success
        
        Args:
            test_name: Name of the test
        
        Returns:
            Path to the captured screenshot
        """
        if config.SCREENSHOT_ON_SUCCESS:
            return self.capture(test_name, "passed")
        return ""
    
    def capture_full_page(self, test_name: str) -> str:
        """
        Capture full page screenshot
        
        Args:
            test_name: Name of the test
        
        Returns:
            Path to the captured screenshot
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{test_name}_fullpage_{timestamp}.png"
        filepath = os.path.join(config.SCREENSHOTS_DIR, filename)
        
        try:
            # Get total page height
            total_height = self.driver.execute_script("return document.body.scrollHeight")
            
            # Set window size to capture full page
            original_size = self.driver.get_window_size()
            self.driver.set_window_size(1920, total_height)
            
            # Capture screenshot
            self.driver.save_screenshot(filepath)
            
            # Restore original window size
            self.driver.set_window_size(original_size['width'], original_size['height'])
            
            test_logger.info(f"Full page screenshot captured: {filepath}")
            return filepath
        except Exception as e:
            test_logger.error(f"Failed to capture full page screenshot: {e}")
            return self.capture(test_name, "fullpage_failed")
    
    def capture_element(self, element, test_name: str, element_name: str = "element") -> str:
        """
        Capture screenshot of specific element
        
        Args:
            element: WebElement to capture
            test_name: Name of the test
            element_name: Name of the element
        
        Returns:
            Path to the captured screenshot
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{test_name}_{element_name}_{timestamp}.png"
        filepath = os.path.join(config.SCREENSHOTS_DIR, filename)
        
        try:
            element.screenshot(filepath)
            test_logger.info(f"Element screenshot captured: {filepath}")
            return filepath
        except Exception as e:
            test_logger.error(f"Failed to capture element screenshot: {e}")
            return ""
    
    def _add_error_annotation(self, filepath: str, error: str):
        """Add error annotation to screenshot (placeholder for future enhancement)"""
        # This could be enhanced with PIL to add text overlays
        pass
    
    def cleanup_old_screenshots(self, days: int = 7):
        """
        Clean up screenshots older than specified days
        
        Args:
            days: Number of days to keep screenshots
        """
        try:
            current_time = time.time()
            cutoff_time = current_time - (days * 86400)  # 86400 seconds in a day
            
            for filename in os.listdir(config.SCREENSHOTS_DIR):
                filepath = os.path.join(config.SCREENSHOTS_DIR, filename)
                if os.path.isfile(filepath):
                    file_time = os.path.getmtime(filepath)
                    if file_time < cutoff_time:
                        os.remove(filepath)
                        test_logger.info(f"Deleted old screenshot: {filename}")
        except Exception as e:
            test_logger.error(f"Failed to cleanup old screenshots: {e}")
