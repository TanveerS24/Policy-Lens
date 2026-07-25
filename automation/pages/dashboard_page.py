"""
Dashboard page object model
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import test_logger


class DashboardPage(BasePage):
    """Dashboard page object"""
    
    # Locators
    DASHBOARD_CONTAINER = (By.ID, "dashboard")
    WELCOME_MESSAGE = (By.CSS_SELECTOR, "[data-testid='welcome-message']")
    STATS_CARDS = (By.CSS_SELECTOR, "[data-testid='stats-card']")
    TOTAL_SCHEMES = (By.CSS_SELECTOR, "[data-testid='total-schemes']")
    TOTAL_USERS = (By.CSS_SELECTOR, "[data-testid='total-users']")
    ACTIVE_SCHEMES = (By.CSS_SELECTOR, "[data-testid='active-schemes']")
    RECENT_ACTIVITY = (By.CSS_SELECTOR, "[data-testid='recent-activity']")
    CHARTS_SECTION = (By.CSS_SELECTOR, "[data-testid='charts-section']")
    SIDEBAR = (By.ID, "sidebar")
    NAVIGATION_MENU = (By.CSS_SELECTOR, "[data-testid='navigation-menu']")
    USER_PROFILE = (By.CSS_SELECTOR, "[data-testid='user-profile']")
    LOGOUT_BUTTON = (By.ID, "logout-button")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = f"{self.base_url}dashboard"
    
    def navigate(self):
        """Navigate to dashboard"""
        self.navigate_to(self.url)
    
    def is_dashboard_loaded(self) -> bool:
        """Check if dashboard is loaded"""
        return self.wait_helper.wait_for_element_visible(self.DASHBOARD_CONTAINER)
    
    def get_welcome_message(self) -> str:
        """Get welcome message"""
        return self.get_text(self.WELCOME_MESSAGE)
    
    def get_total_schemes_count(self) -> str:
        """Get total schemes count"""
        return self.get_text(self.TOTAL_SCHEMES)
    
    def get_total_users_count(self) -> str:
        """Get total users count"""
        return self.get_text(self.TOTAL_USERS)
    
    def get_active_schemes_count(self) -> str:
        """Get active schemes count"""
        return self.get_text(self.ACTIVE_SCHEMES)
    
    def get_stats_cards_count(self) -> int:
        """Get number of stats cards"""
        return len(self.find_elements(self.STATS_CARDS))
    
    def is_recent_activity_visible(self) -> bool:
        """Check if recent activity section is visible"""
        return self.is_displayed(self.RECENT_ACTIVITY)
    
    def is_charts_section_visible(self) -> bool:
        """Check if charts section is visible"""
        return self.is_displayed(self.CHARTS_SECTION)
    
    def is_sidebar_visible(self) -> bool:
        """Check if sidebar is visible"""
        return self.is_displayed(self.SIDEBAR)
    
    def click_logout(self):
        """Click logout button"""
        test_logger.info("Clicking logout button")
        self.click(self.LOGOUT_BUTTON)
    
    def is_user_profile_visible(self) -> bool:
        """Check if user profile is visible"""
        return self.is_displayed(self.USER_PROFILE)
    
    def get_navigation_menu_items(self) -> list:
        """Get navigation menu items"""
        elements = self.find_elements(self.NAVIGATION_MENU)
        return [element.text for element in elements]
