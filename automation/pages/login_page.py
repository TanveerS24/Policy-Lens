"""
Login page object model
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import test_logger


class LoginPage(BasePage):
    """Login page object"""
    
    # Locators
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    LOGIN_FORM = (By.ID, "login-form")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-testid='error-message']")
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, "Forgot Password")
    REMEMBER_ME_CHECKBOX = (By.ID, "remember-me")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = f"{self.base_url}login"
    
    def navigate(self):
        """Navigate to login page"""
        self.navigate_to(self.url)
    
    def enter_email(self, email: str):
        """
        Enter email address
        
        Args:
            email: Email address
        """
        test_logger.info(f"Entering email: {email}")
        self.send_keys(self.EMAIL_INPUT, email)
    
    def enter_password(self, password: str):
        """
        Enter password
        
        Args:
            password: Password
        """
        test_logger.info("Entering password")
        self.send_keys(self.PASSWORD_INPUT, password)
    
    def click_login(self):
        """Click login button"""
        test_logger.info("Clicking login button")
        self.click(self.LOGIN_BUTTON)
    
    def login(self, email: str, password: str):
        """
        Perform login
        
        Args:
            email: Email address
            password: Password
        """
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()
    
    def is_login_page_loaded(self) -> bool:
        """Check if login page is loaded"""
        return self.wait_helper.wait_for_element_visible(self.LOGIN_FORM)
    
    def get_error_message(self) -> str:
        """Get error message text"""
        if self.is_displayed(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return ""
    
    def click_forgot_password(self):
        """Click forgot password link"""
        test_logger.info("Clicking forgot password link")
        self.click(self.FORGOT_PASSWORD_LINK)
    
    def check_remember_me(self):
        """Check remember me checkbox"""
        test_logger.info("Checking remember me")
        if not self.is_selected(self.REMEMBER_ME_CHECKBOX):
            self.click(self.REMEMBER_ME_CHECKBOX)
    
    def uncheck_remember_me(self):
        """Uncheck remember me checkbox"""
        test_logger.info("Unchecking remember me")
        if self.is_selected(self.REMEMBER_ME_CHECKBOX):
            self.click(self.REMEMBER_ME_CHECKBOX)
