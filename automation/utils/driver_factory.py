"""
WebDriver factory for creating browser instances
"""

import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from config.config import config
from utils.logger import test_logger


class DriverFactory:
    """Factory class for creating WebDriver instances"""
    
    @staticmethod
    def get_driver(browser: str = None, headless: bool = None) -> webdriver:
        """
        Get WebDriver instance based on configuration
        
        Args:
            browser: Browser type (chrome, firefox, edge)
            headless: Whether to run in headless mode
        
        Returns:
            WebDriver instance
        """
        browser = browser or config.BROWSER
        headless = headless if headless is not None else config.HEADLESS
        
        test_logger.info(f"Creating {browser} driver (headless={headless})")
        
        if browser.lower() == "chrome":
            return DriverFactory._get_chrome_driver(headless)
        elif browser.lower() == "firefox":
            return DriverFactory._get_firefox_driver(headless)
        elif browser.lower() == "edge":
            return DriverFactory._get_edge_driver(headless)
        else:
            raise ValueError(f"Unsupported browser: {browser}")
    
    @staticmethod
    def _get_chrome_driver(headless: bool) -> webdriver.Chrome:
        """Create Chrome WebDriver"""
        options = ChromeOptions()
        
        if headless:
            options.add_argument("--headless=new")
        
        # Common Chrome options
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-notifications")
        options.add_argument("--start-maximized")
        options.add_argument("--window-size=1920,1080")
        
        # Set user agent
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # Ignore SSL errors (for testing only)
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--allow-running-insecure-content")
        
        # Disable automation flags
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        # Set timeouts
        driver.implicitly_wait(config.IMPLICIT_WAIT)
        driver.set_page_load_timeout(config.PAGE_LOAD_TIMEOUT)
        
        return driver
    
    @staticmethod
    def _get_firefox_driver(headless: bool) -> webdriver.Firefox:
        """Create Firefox WebDriver"""
        options = FirefoxOptions()
        
        if headless:
            options.add_argument("--headless")
        
        options.set_preference("dom.webnotifications.enabled", False)
        options.set_preference("network.stricttransportsecurity.preloadlist", False)
        
        driver = webdriver.Firefox(
            service=Service(GeckoDriverManager().install()),
            options=options
        )
        
        driver.implicitly_wait(config.IMPLICIT_WAIT)
        driver.set_page_load_timeout(config.PAGE_LOAD_TIMEOUT)
        
        return driver
    
    @staticmethod
    def _get_edge_driver(headless: bool) -> webdriver.Edge:
        """Create Edge WebDriver"""
        options = EdgeOptions()
        
        if headless:
            options.add_argument("--headless=new")
        
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--start-maximized")
        options.add_argument("--window-size=1920,1080")
        
        service = Service(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)
        
        driver.implicitly_wait(config.IMPLICIT_WAIT)
        driver.set_page_load_timeout(config.PAGE_LOAD_TIMEOUT)
        
        return driver
    
    @staticmethod
    def quit_driver(driver: webdriver):
        """Safely quit WebDriver"""
        try:
            if driver:
                driver.quit()
                test_logger.info("Driver quit successfully")
        except Exception as e:
            test_logger.error(f"Error quitting driver: {e}")
