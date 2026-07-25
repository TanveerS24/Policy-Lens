"""
Schemes management page object model
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import test_logger


class SchemesPage(BasePage):
    """Schemes management page object"""
    
    # Locators
    SCHEMES_CONTAINER = (By.ID, "schemes-page")
    SCHEMES_TABLE = (By.ID, "schemes-table")
    SCHEMES_LIST = (By.CSS_SELECTOR, "[data-testid='schemes-list']")
    ADD_SCHEME_BUTTON = (By.ID, "add-scheme-button")
    SEARCH_INPUT = (By.ID, "search-input")
    FILTER_BUTTON = (By.ID, "filter-button")
    EXPORT_BUTTON = (By.ID, "export-button")
    SCHEME_ROW = (By.CSS_SELECTOR, "[data-testid='scheme-row']")
    SCHEME_NAME = (By.CSS_SELECTOR, "[data-testid='scheme-name']")
    SCHEME_STATUS = (By.CSS_SELECTOR, "[data-testid='scheme-status']")
    SCHEME_TYPE = (By.CSS_SELECTOR, "[data-testid='scheme-type']")
    EDIT_BUTTON = (By.CSS_SELECTOR, "[data-testid='edit-button']")
    DELETE_BUTTON = (By.CSS_SELECTOR, "[data-testid='delete-button']")
    VIEW_BUTTON = (By.CSS_SELECTOR, "[data-testid='view-button']")
    PAGINATION = (By.CSS_SELECTOR, "[data-testid='pagination']")
    NEXT_PAGE = (By.CSS_SELECTOR, "[data-testid='next-page']")
    PREV_PAGE = (By.CSS_SELECTOR, "[data-testid='prev-page']")
    PAGE_NUMBER = (By.CSS_SELECTOR, "[data-testid='page-number']")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = f"{self.base_url}schemes"
    
    def navigate(self):
        """Navigate to schemes page"""
        self.navigate_to(self.url)
    
    def is_schemes_page_loaded(self) -> bool:
        """Check if schemes page is loaded"""
        return self.wait_helper.wait_for_element_visible(self.SCHEMES_CONTAINER)
    
    def click_add_scheme(self):
        """Click add scheme button"""
        test_logger.info("Clicking add scheme button")
        self.click(self.ADD_SCHEME_BUTTON)
    
    def search_scheme(self, search_term: str):
        """
        Search for scheme
        
        Args:
            search_term: Search term
        """
        test_logger.info(f"Searching for scheme: {search_term}")
        self.send_keys(self.SEARCH_INPUT, search_term)
    
    def click_filter(self):
        """Click filter button"""
        test_logger.info("Clicking filter button")
        self.click(self.FILTER_BUTTON)
    
    def click_export(self):
        """Click export button"""
        test_logger.info("Clicking export button")
        self.click(self.EXPORT_BUTTON)
    
    def get_schemes_count(self) -> int:
        """Get number of schemes displayed"""
        return len(self.find_elements(self.SCHEME_ROW))
    
    def get_scheme_names(self) -> list:
        """Get list of scheme names"""
        elements = self.find_elements(self.SCHEME_NAME)
        return [element.text for element in elements]
    
    def click_edit_scheme(self, index: int = 0):
        """
        Click edit button for scheme at index
        
        Args:
            index: Index of scheme row
        """
        test_logger.info(f"Clicking edit button for scheme at index {index}")
        edit_buttons = self.find_elements(self.EDIT_BUTTON)
        if index < len(edit_buttons):
            edit_buttons[index].click()
    
    def click_delete_scheme(self, index: int = 0):
        """
        Click delete button for scheme at index
        
        Args:
            index: Index of scheme row
        """
        test_logger.info(f"Clicking delete button for scheme at index {index}")
        delete_buttons = self.find_elements(self.DELETE_BUTTON)
        if index < len(delete_buttons):
            delete_buttons[index].click()
    
    def click_view_scheme(self, index: int = 0):
        """
        Click view button for scheme at index
        
        Args:
            index: Index of scheme row
        """
        test_logger.info(f"Clicking view button for scheme at index {index}")
        view_buttons = self.find_elements(self.VIEW_BUTTON)
        if index < len(view_buttons):
            view_buttons[index].click()
    
    def get_scheme_status(self, index: int = 0) -> str:
        """
        Get scheme status at index
        
        Args:
            index: Index of scheme row
        
        Returns:
            Scheme status
        """
        status_elements = self.find_elements(self.SCHEME_STATUS)
        if index < len(status_elements):
            return status_elements[index].text
        return ""
    
    def get_scheme_type(self, index: int = 0) -> str:
        """
        Get scheme type at index
        
        Args:
            index: Index of scheme row
        
        Returns:
            Scheme type
        """
        type_elements = self.find_elements(self.SCHEME_TYPE)
        if index < len(type_elements):
            return type_elements[index].text
        return ""
    
    def click_next_page(self):
        """Click next page button"""
        test_logger.info("Clicking next page")
        self.click(self.NEXT_PAGE)
    
    def click_prev_page(self):
        """Click previous page button"""
        test_logger.info("Clicking previous page")
        self.click(self.PREV_PAGE)
    
    def get_current_page_number(self) -> str:
        """Get current page number"""
        return self.get_text(self.PAGE_NUMBER)
    
    def is_pagination_visible(self) -> bool:
        """Check if pagination is visible"""
        return self.is_displayed(self.PAGINATION)
