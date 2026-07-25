"""
Users management page object model
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import test_logger


class UsersPage(BasePage):
    """Users management page object"""
    
    # Locators
    USERS_CONTAINER = (By.ID, "users-page")
    USERS_TABLE = (By.ID, "users-table")
    USERS_LIST = (By.CSS_SELECTOR, "[data-testid='users-list']")
    ADD_USER_BUTTON = (By.ID, "add-user-button")
    SEARCH_INPUT = (By.ID, "search-input")
    FILTER_BUTTON = (By.ID, "filter-button")
    EXPORT_BUTTON = (By.ID, "export-button")
    USER_ROW = (By.CSS_SELECTOR, "[data-testid='user-row']")
    USER_NAME = (By.CSS_SELECTOR, "[data-testid='user-name']")
    USER_EMAIL = (By.CSS_SELECTOR, "[data-testid='user-email']")
    USER_STATUS = (By.CSS_SELECTOR, "[data-testid='user-status']")
    USER_ROLE = (By.CSS_SELECTOR, "[data-testid='user-role']")
    EDIT_BUTTON = (By.CSS_SELECTOR, "[data-testid='edit-user-button']")
    DELETE_BUTTON = (By.CSS_SELECTOR, "[data-testid='delete-user-button']")
    VIEW_BUTTON = (By.CSS_SELECTOR, "[data-testid='view-user-button']")
    ACTIVATE_BUTTON = (By.CSS_SELECTOR, "[data-testid='activate-button']")
    DEACTIVATE_BUTTON = (By.CSS_SELECTOR, "[data-testid='deactivate-button']")
    PAGINATION = (By.CSS_SELECTOR, "[data-testid='pagination']")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = f"{self.base_url}users"
    
    def navigate(self):
        """Navigate to users page"""
        self.navigate_to(self.url)
    
    def is_users_page_loaded(self) -> bool:
        """Check if users page is loaded"""
        return self.wait_helper.wait_for_element_visible(self.USERS_CONTAINER)
    
    def click_add_user(self):
        """Click add user button"""
        test_logger.info("Clicking add user button")
        self.click(self.ADD_USER_BUTTON)
    
    def search_user(self, search_term: str):
        """
        Search for user
        
        Args:
            search_term: Search term
        """
        test_logger.info(f"Searching for user: {search_term}")
        self.send_keys(self.SEARCH_INPUT, search_term)
    
    def click_filter(self):
        """Click filter button"""
        test_logger.info("Clicking filter button")
        self.click(self.FILTER_BUTTON)
    
    def click_export(self):
        """Click export button"""
        test_logger.info("Clicking export button")
        self.click(self.EXPORT_BUTTON)
    
    def get_users_count(self) -> int:
        """Get number of users displayed"""
        return len(self.find_elements(self.USER_ROW))
    
    def get_user_names(self) -> list:
        """Get list of user names"""
        elements = self.find_elements(self.USER_NAME)
        return [element.text for element in elements]
    
    def get_user_emails(self) -> list:
        """Get list of user emails"""
        elements = self.find_elements(self.USER_EMAIL)
        return [element.text for element in elements]
    
    def click_edit_user(self, index: int = 0):
        """
        Click edit button for user at index
        
        Args:
            index: Index of user row
        """
        test_logger.info(f"Clicking edit button for user at index {index}")
        edit_buttons = self.find_elements(self.EDIT_BUTTON)
        if index < len(edit_buttons):
            edit_buttons[index].click()
    
    def click_delete_user(self, index: int = 0):
        """
        Click delete button for user at index
        
        Args:
            index: Index of user row
        """
        test_logger.info(f"Clicking delete button for user at index {index}")
        delete_buttons = self.find_elements(self.DELETE_BUTTON)
        if index < len(delete_buttons):
            delete_buttons[index].click()
    
    def click_view_user(self, index: int = 0):
        """
        Click view button for user at index
        
        Args:
            index: Index of user row
        """
        test_logger.info(f"Clicking view button for user at index {index}")
        view_buttons = self.find_elements(self.VIEW_BUTTON)
        if index < len(view_buttons):
            view_buttons[index].click()
    
    def click_activate_user(self, index: int = 0):
        """
        Click activate button for user at index
        
        Args:
            index: Index of user row
        """
        test_logger.info(f"Clicking activate button for user at index {index}")
        activate_buttons = self.find_elements(self.ACTIVATE_BUTTON)
        if index < len(activate_buttons):
            activate_buttons[index].click()
    
    def click_deactivate_user(self, index: int = 0):
        """
        Click deactivate button for user at index
        
        Args:
            index: Index of user row
        """
        test_logger.info(f"Clicking deactivate button for user at index {index}")
        deactivate_buttons = self.find_elements(self.DEACTIVATE_BUTTON)
        if index < len(deactivate_buttons):
            deactivate_buttons[index].click()
    
    def get_user_status(self, index: int = 0) -> str:
        """
        Get user status at index
        
        Args:
            index: Index of user row
        
        Returns:
            User status
        """
        status_elements = self.find_elements(self.USER_STATUS)
        if index < len(status_elements):
            return status_elements[index].text
        return ""
    
    def get_user_role(self, index: int = 0) -> str:
        """
        Get user role at index
        
        Args:
            index: Index of user row
        
        Returns:
            User role
        """
        role_elements = self.find_elements(self.USER_ROLE)
        if index < len(role_elements):
            return role_elements[index].text
        return ""
