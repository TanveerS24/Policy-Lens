"""
Admins management page object model
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import test_logger


class AdminsPage(BasePage):
    """Admins management page object"""
    
    # Locators
    ADMINS_CONTAINER = (By.ID, "admins-page")
    ADMINS_TABLE = (By.ID, "admins-table")
    ADMINS_LIST = (By.CSS_SELECTOR, "[data-testid='admins-list']")
    ADD_ADMIN_BUTTON = (By.ID, "add-admin-button")
    SEARCH_INPUT = (By.ID, "search-input")
    FILTER_BUTTON = (By.ID, "filter-button")
    EXPORT_BUTTON = (By.ID, "export-button")
    ADMIN_ROW = (By.CSS_SELECTOR, "[data-testid='admin-row']")
    ADMIN_NAME = (By.CSS_SELECTOR, "[data-testid='admin-name']")
    ADMIN_EMAIL = (By.CSS_SELECTOR, "[data-testid='admin-email']")
    ADMIN_ROLE = (By.CSS_SELECTOR, "[data-testid='admin-role']")
    ADMIN_STATUS = (By.CSS_SELECTOR, "[data-testid='admin-status']")
    EDIT_BUTTON = (By.CSS_SELECTOR, "[data-testid='edit-admin-button']")
    DELETE_BUTTON = (By.CSS_SELECTOR, "[data-testid='delete-admin-button']")
    VIEW_BUTTON = (By.CSS_SELECTOR, "[data-testid='view-admin-button']")
    ROLE_SELECT = (By.CSS_SELECTOR, "[data-testid='role-select']")
    PAGINATION = (By.CSS_SELECTOR, "[data-testid='pagination']")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = f"{self.base_url}admins"
    
    def navigate(self):
        """Navigate to admins page"""
        self.navigate_to(self.url)
    
    def is_admins_page_loaded(self) -> bool:
        """Check if admins page is loaded"""
        return self.wait_helper.wait_for_element_visible(self.ADMINS_CONTAINER)
    
    def click_add_admin(self):
        """Click add admin button"""
        test_logger.info("Clicking add admin button")
        self.click(self.ADD_ADMIN_BUTTON)
    
    def search_admin(self, search_term: str):
        """
        Search for admin
        
        Args:
            search_term: Search term
        """
        test_logger.info(f"Searching for admin: {search_term}")
        self.send_keys(self.SEARCH_INPUT, search_term)
    
    def click_filter(self):
        """Click filter button"""
        test_logger.info("Clicking filter button")
        self.click(self.FILTER_BUTTON)
    
    def click_export(self):
        """Click export button"""
        test_logger.info("Clicking export button")
        self.click(self.EXPORT_BUTTON)
    
    def get_admins_count(self) -> int:
        """Get number of admins displayed"""
        return len(self.find_elements(self.ADMIN_ROW))
    
    def get_admin_names(self) -> list:
        """Get list of admin names"""
        elements = self.find_elements(self.ADMIN_NAME)
        return [element.text for element in elements]
    
    def get_admin_emails(self) -> list:
        """Get list of admin emails"""
        elements = self.find_elements(self.ADMIN_EMAIL)
        return [element.text for element in elements]
    
    def click_edit_admin(self, index: int = 0):
        """
        Click edit button for admin at index
        
        Args:
            index: Index of admin row
        """
        test_logger.info(f"Clicking edit button for admin at index {index}")
        edit_buttons = self.find_elements(self.EDIT_BUTTON)
        if index < len(edit_buttons):
            edit_buttons[index].click()
    
    def click_delete_admin(self, index: int = 0):
        """
        Click delete button for admin at index
        
        Args:
            index: Index of admin row
        """
        test_logger.info(f"Clicking delete button for admin at index {index}")
        delete_buttons = self.find_elements(self.DELETE_BUTTON)
        if index < len(delete_buttons):
            delete_buttons[index].click()
    
    def click_view_admin(self, index: int = 0):
        """
        Click view button for admin at index
        
        Args:
            index: Index of admin row
        """
        test_logger.info(f"Clicking view button for admin at index {index}")
        view_buttons = self.find_elements(self.VIEW_BUTTON)
        if index < len(view_buttons):
            view_buttons[index].click()
    
    def get_admin_role(self, index: int = 0) -> str:
        """
        Get admin role at index
        
        Args:
            index: Index of admin row
        
        Returns:
            Admin role
        """
        role_elements = self.find_elements(self.ADMIN_ROLE)
        if index < len(role_elements):
            return role_elements[index].text
        return ""
    
    def get_admin_status(self, index: int = 0) -> str:
        """
        Get admin status at index
        
        Args:
            index: Index of admin row
        
        Returns:
            Admin status
        """
        status_elements = self.find_elements(self.ADMIN_STATUS)
        if index < len(status_elements):
            return status_elements[index].text
        return ""
    
    def select_admin_role_filter(self, role: str):
        """
        Select admin role filter
        
        Args:
            role: Role to filter by
        """
        test_logger.info(f"Selecting role filter: {role}")
        self.select_dropdown_by_text(self.ROLE_SELECT, role)
