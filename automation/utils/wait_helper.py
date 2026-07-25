"""
Wait helper utilities for explicit waits
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException
from config.config import config
from utils.logger import test_logger


class WaitHelper:
    """Helper class for explicit waits"""
    
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, config.EXPLICIT_WAIT)
    
    def wait_for_element_visible(self, locator: tuple, timeout: int = None) -> bool:
        """
        Wait for element to be visible
        
        Args:
            locator: Element locator (By.ID, "element_id")
            timeout: Custom timeout (uses config if not provided)
        
        Returns:
            True if element is visible, False otherwise
        """
        try:
            wait = WebDriverWait(self.driver, timeout or config.EXPLICIT_WAIT)
            wait.until(EC.visibility_of_element_located(locator))
            test_logger.debug(f"Element visible: {locator}")
            return True
        except TimeoutException:
            test_logger.warning(f"Element not visible within timeout: {locator}")
            return False
    
    def wait_for_element_present(self, locator: tuple, timeout: int = None) -> bool:
        """
        Wait for element to be present in DOM
        
        Args:
            locator: Element locator
            timeout: Custom timeout
        
        Returns:
            True if element is present, False otherwise
        """
        try:
            wait = WebDriverWait(self.driver, timeout or config.EXPLICIT_WAIT)
            wait.until(EC.presence_of_element_located(locator))
            test_logger.debug(f"Element present: {locator}")
            return True
        except TimeoutException:
            test_logger.warning(f"Element not present within timeout: {locator}")
            return False
    
    def wait_for_element_clickable(self, locator: tuple, timeout: int = None) -> bool:
        """
        Wait for element to be clickable
        
        Args:
            locator: Element locator
            timeout: Custom timeout
        
        Returns:
            True if element is clickable, False otherwise
        """
        try:
            wait = WebDriverWait(self.driver, timeout or config.EXPLICIT_WAIT)
            wait.until(EC.element_to_be_clickable(locator))
            test_logger.debug(f"Element clickable: {locator}")
            return True
        except TimeoutException:
            test_logger.warning(f"Element not clickable within timeout: {locator}")
            return False
    
    def wait_for_text_present(self, locator: tuple, text: str, timeout: int = None) -> bool:
        """
        Wait for text to be present in element
        
        Args:
            locator: Element locator
            text: Expected text
            timeout: Custom timeout
        
        Returns:
            True if text is present, False otherwise
        """
        try:
            wait = WebDriverWait(self.driver, timeout or config.EXPLICIT_WAIT)
            wait.until(EC.text_to_be_present_in_element(locator, text))
            test_logger.debug(f"Text present in element: {locator} - '{text}'")
            return True
        except TimeoutException:
            test_logger.warning(f"Text not present within timeout: {locator} - '{text}'")
            return False
    
    def wait_for_title_contains(self, title: str, timeout: int = None) -> bool:
        """
        Wait for page title to contain text
        
        Args:
            title: Expected title text
            timeout: Custom timeout
        
        Returns:
            True if title contains text, False otherwise
        """
        try:
            wait = WebDriverWait(self.driver, timeout or config.EXPLICIT_WAIT)
            wait.until(EC.title_contains(title))
            test_logger.debug(f"Title contains: '{title}'")
            return True
        except TimeoutException:
            test_logger.warning(f"Title does not contain within timeout: '{title}'")
            return False
    
    def wait_for_url_contains(self, url: str, timeout: int = None) -> bool:
        """
        Wait for URL to contain text
        
        Args:
            url: Expected URL text
            timeout: Custom timeout
        
        Returns:
            True if URL contains text, False otherwise
        """
        try:
            wait = WebDriverWait(self.driver, timeout or config.EXPLICIT_WAIT)
            wait.until(EC.url_contains(url))
            test_logger.debug(f"URL contains: '{url}'")
            return True
        except TimeoutException:
            test_logger.warning(f"URL does not contain within timeout: '{url}'")
            return False
    
    def wait_for_element_invisible(self, locator: tuple, timeout: int = None) -> bool:
        """
        Wait for element to be invisible
        
        Args:
            locator: Element locator
            timeout: Custom timeout
        
        Returns:
            True if element is invisible, False otherwise
        """
        try:
            wait = WebDriverWait(self.driver, timeout or config.EXPLICIT_WAIT)
            wait.until(EC.invisibility_of_element_located(locator))
            test_logger.debug(f"Element invisible: {locator}")
            return True
        except TimeoutException:
            test_logger.warning(f"Element not invisible within timeout: {locator}")
            return False
    
    def wait_for_staleness(self, element, timeout: int = None) -> bool:
        """
        Wait for element to become stale
        
        Args:
            element: WebElement
            timeout: Custom timeout
        
        Returns:
            True if element is stale, False otherwise
        """
        try:
            wait = WebDriverWait(self.driver, timeout or config.EXPLICIT_WAIT)
            wait.until(EC.staleness_of(element))
            test_logger.debug("Element became stale")
            return True
        except TimeoutException:
            test_logger.warning("Element did not become stale within timeout")
            return False
    
    def wait_for_page_load(self, timeout: int = None) -> bool:
        """
        Wait for page to fully load
        
        Args:
            timeout: Custom timeout
        
        Returns:
            True if page loaded, False otherwise
        """
        try:
            wait = WebDriverWait(self.driver, timeout or config.PAGE_LOAD_TIMEOUT)
            wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
            test_logger.debug("Page fully loaded")
            return True
        except TimeoutException:
            test_logger.warning("Page did not fully load within timeout")
            return False
    
    def wait_for_alert(self, timeout: int = None) -> bool:
        """
        Wait for alert to be present
        
        Args:
            timeout: Custom timeout
        
        Returns:
            True if alert is present, False otherwise
        """
        try:
            wait = WebDriverWait(self.driver, timeout or config.EXPLICIT_WAIT)
            wait.until(EC.alert_is_present())
            test_logger.debug("Alert present")
            return True
        except TimeoutException:
            test_logger.warning("Alert not present within timeout")
            return False
    
    def wait_for_frame_to_be_available(self, locator: tuple, timeout: int = None) -> bool:
        """
        Wait for frame to be available
        
        Args:
            locator: Frame locator
            timeout: Custom timeout
        
        Returns:
            True if frame is available, False otherwise
        """
        try:
            wait = WebDriverWait(self.driver, timeout or config.EXPLICIT_WAIT)
            wait.until(EC.frame_to_be_available_and_switch_to_it(locator))
            test_logger.debug(f"Frame available: {locator}")
            return True
        except TimeoutException:
            test_logger.warning(f"Frame not available within timeout: {locator}")
            return False
