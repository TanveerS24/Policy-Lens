"""
Base page class with common functionality
"""

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from config.config import config
from utils.logger import test_logger
from utils.screenshot import ScreenshotManager
from utils.wait_helper import WaitHelper


class BasePage:
    """Base page class with common page operations"""
    
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.screenshot_manager = ScreenshotManager(driver)
        self.wait_helper = WaitHelper(driver)
        self.base_url = config.BASE_URL
    
    def navigate_to(self, url: str = None):
        """
        Navigate to URL
        
        Args:
            url: URL to navigate to (uses base_url if not provided)
        """
        target_url = url or self.base_url
        test_logger.info(f"Navigating to: {target_url}")
        self.driver.get(target_url)
        self.wait_helper.wait_for_page_load()
    
    def get_current_url(self) -> str:
        """Get current URL"""
        return self.driver.current_url
    
    def get_title(self) -> str:
        """Get page title"""
        return self.driver.title
    
    def find_element(self, locator: tuple):
        """
        Find element by locator
        
        Args:
            locator: Element locator tuple (By.ID, "element_id")
        
        Returns:
            WebElement
        """
        return self.driver.find_element(*locator)
    
    def find_elements(self, locator: tuple):
        """
        Find multiple elements by locator
        
        Args:
            locator: Element locator tuple
        
        Returns:
            List of WebElements
        """
        return self.driver.find_elements(*locator)
    
    def click(self, locator: tuple):
        """
        Click on element
        
        Args:
            locator: Element locator
        """
        test_logger.debug(f"Clicking element: {locator}")
        if self.wait_helper.wait_for_element_clickable(locator):
            self.find_element(locator).click()
        else:
            raise Exception(f"Element not clickable: {locator}")
    
    def send_keys(self, locator: tuple, text: str, clear: bool = True):
        """
        Send keys to element
        
        Args:
            locator: Element locator
            text: Text to send
            clear: Whether to clear field before sending keys
        """
        test_logger.debug(f"Sending keys to element: {locator}")
        element = self.find_element(locator)
        if clear:
            element.clear()
        element.send_keys(text)
    
    def get_text(self, locator: tuple) -> str:
        """
        Get text from element
        
        Args:
            locator: Element locator
        
        Returns:
            Element text
        """
        return self.find_element(locator).text
    
    def get_attribute(self, locator: tuple, attribute: str) -> str:
        """
        Get attribute value from element
        
        Args:
            locator: Element locator
            attribute: Attribute name
        
        Returns:
            Attribute value
        """
        return self.find_element(locator).get_attribute(attribute)
    
    def is_displayed(self, locator: tuple) -> bool:
        """
        Check if element is displayed
        
        Args:
            locator: Element locator
        
        Returns:
            True if displayed, False otherwise
        """
        try:
            return self.find_element(locator).is_displayed()
        except Exception:
            return False
    
    def is_enabled(self, locator: tuple) -> bool:
        """
        Check if element is enabled
        
        Args:
            locator: Element locator
        
        Returns:
            True if enabled, False otherwise
        """
        try:
            return self.find_element(locator).is_enabled()
        except Exception:
            return False
    
    def is_selected(self, locator: tuple) -> bool:
        """
        Check if element is selected
        
        Args:
            locator: Element locator
        
        Returns:
            True if selected, False otherwise
        """
        try:
            return self.find_element(locator).is_selected()
        except Exception:
            return False
    
    def select_dropdown_by_value(self, locator: tuple, value: str):
        """
        Select dropdown option by value
        
        Args:
            locator: Dropdown element locator
            value: Option value to select
        """
        test_logger.debug(f"Selecting dropdown value: {value}")
        select = Select(self.find_element(locator))
        select.select_by_value(value)
    
    def select_dropdown_by_text(self, locator: tuple, text: str):
        """
        Select dropdown option by visible text
        
        Args:
            locator: Dropdown element locator
            text: Option text to select
        """
        test_logger.debug(f"Selecting dropdown text: {text}")
        select = Select(self.find_element(locator))
        select.select_by_visible_text(text)
    
    def select_dropdown_by_index(self, locator: tuple, index: int):
        """
        Select dropdown option by index
        
        Args:
            locator: Dropdown element locator
            index: Option index to select
        """
        test_logger.debug(f"Selecting dropdown index: {index}")
        select = Select(self.find_element(locator))
        select.select_by_index(index)
    
    def hover_over_element(self, locator: tuple):
        """
        Hover over element
        
        Args:
            locator: Element locator
        """
        from selenium.webdriver.common.action_chains import ActionChains
        test_logger.debug(f"Hovering over element: {locator}")
        actions = ActionChains(self.driver)
        actions.move_to_element(self.find_element(locator)).perform()
    
    def scroll_to_element(self, locator: tuple):
        """
        Scroll to element
        
        Args:
            locator: Element locator
        """
        test_logger.debug(f"Scrolling to element: {locator}")
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
    
    def scroll_to_top(self):
        """Scroll to top of page"""
        test_logger.debug("Scrolling to top of page")
        self.driver.execute_script("window.scrollTo(0, 0);")
    
    def scroll_to_bottom(self):
        """Scroll to bottom of page"""
        test_logger.debug("Scrolling to bottom of page")
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    def execute_javascript(self, script: str, *args):
        """
        Execute JavaScript
        
        Args:
            script: JavaScript code to execute
            *args: Arguments to pass to script
        
        Returns:
            Script execution result
        """
        return self.driver.execute_script(script, *args)
    
    def switch_to_frame(self, locator: tuple):
        """
        Switch to iframe
        
        Args:
            locator: Frame locator
        """
        test_logger.debug(f"Switching to frame: {locator}")
        self.driver.switch_to.frame(self.find_element(locator))
    
    def switch_to_default_content(self):
        """Switch to default content"""
        test_logger.debug("Switching to default content")
        self.driver.switch_to.default_content()
    
    def switch_to_window(self, window_handle: str):
        """
        Switch to window/tab
        
        Args:
            window_handle: Window handle
        """
        test_logger.debug(f"Switching to window: {window_handle}")
        self.driver.switch_to.window(window_handle)
    
    def get_window_handles(self) -> list:
        """Get all window handles"""
        return self.driver.window_handles
    
    def open_new_tab(self):
        """Open new tab"""
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[-1])
    
    def close_current_tab(self):
        """Close current tab"""
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
    
    def refresh_page(self):
        """Refresh current page"""
        test_logger.debug("Refreshing page")
        self.driver.refresh()
    
    def go_back(self):
        """Go back in browser history"""
        test_logger.debug("Going back")
        self.driver.back()
    
    def go_forward(self):
        """Go forward in browser history"""
        test_logger.debug("Going forward")
        self.driver.forward()
    
    def accept_alert(self):
        """Accept browser alert"""
        test_logger.debug("Accepting alert")
        self.driver.switch_to.alert.accept()
    
    def dismiss_alert(self):
        """Dismiss browser alert"""
        test_logger.debug("Dismissing alert")
        self.driver.switch_to.alert.dismiss()
    
    def get_alert_text(self) -> str:
        """Get alert text"""
        return self.driver.switch_to.alert.text
    
    def take_screenshot(self, test_name: str, status: str = "info") -> str:
        """
        Take screenshot
        
        Args:
            test_name: Test name
            status: Test status
        
        Returns:
            Screenshot path
        """
        return self.screenshot_manager.capture(test_name, status)
