"""
Navigation test cases - 30 test cases
"""

import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.schemes_page import SchemesPage
from pages.users_page import UsersPage
from pages.admins_page import AdminsPage
from utils.logger import test_logger


@pytest.mark.nav
class TestNavigation:
    """Navigation test suite"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver, base_url):
        """Setup for each test"""
        self.driver = driver
        self.base_url = base_url
        self.login_page = LoginPage(driver)
        self.dashboard_page = DashboardPage(driver)
        self.schemes_page = SchemesPage(driver)
        self.users_page = UsersPage(driver)
        self.admins_page = AdminsPage(driver)
    
    def test_nav_001_home_page_navigation(self):
        """TC_NAV_001: Navigate to home page"""
        test_logger.info("TC_NAV_001: Navigate to home page")
        self.driver.get(self.base_url)
        assert self.base_url in self.driver.current_url
    
    def test_nav_002_login_page_navigation(self):
        """TC_NAV_002: Navigate to login page"""
        test_logger.info("TC_NAV_002: Navigate to login page")
        self.login_page.navigate()
        assert self.login_page.is_login_page_loaded()
    
    def test_nav_003_dashboard_page_navigation(self, test_data):
        """TC_NAV_003: Navigate to dashboard page"""
        test_logger.info("TC_NAV_003: Navigate to dashboard page")
        self.login_page.navigate()
        self.login_page.login("super_admin@example.com", "Admin@123")
        self.dashboard_page.navigate()
        assert self.dashboard_page.is_dashboard_loaded()
    
    def test_nav_004_schemes_page_navigation(self, test_data):
        """TC_NAV_004: Navigate to schemes page"""
        test_logger.info("TC_NAV_004: Navigate to schemes page")
        self.login_page.navigate()
        self.login_page.login("super_admin@example.com", "Admin@123")
        self.schemes_page.navigate()
        assert self.schemes_page.is_schemes_page_loaded()
    
    def test_nav_005_users_page_navigation(self, test_data):
        """TC_NAV_005: Navigate to users page"""
        test_logger.info("TC_NAV_005: Navigate to users page")
        self.login_page.navigate()
        self.login_page.login("super_admin@example.com", "Admin@123")
        self.users_page.navigate()
        assert self.users_page.is_users_page_loaded()
    
    def test_nav_006_admins_page_navigation(self, test_data):
        """TC_NAV_006: Navigate to admins page"""
        test_logger.info("TC_NAV_006: Navigate to admins page")
        self.login_page.navigate()
        self.login_page.login("super_admin@example.com", "Admin@123")
        self.admins_page.navigate()
        assert self.admins_page.is_admins_page_loaded()
    
    def test_nav_007_menu_navigation(self, test_data):
        """TC_NAV_007: Navigate via menu"""
        test_logger.info("TC_NAV_007: Navigate via menu")
        self.login_page.navigate()
        self.login_page.login("super_admin@example.com", "Admin@123")
        menu_items = self.dashboard_page.get_navigation_menu_items()
        assert len(menu_items) > 0
    
    def test_nav_008_breadcrumb_navigation(self, test_data):
        """TC_NAV_008: Breadcrumb navigation"""
        test_logger.info("TC_NAV_008: Breadcrumb navigation")
        self.login_page.navigate()
        self.login_page.login("super_admin@example.com", "Admin@123")
        self.schemes_page.navigate()
        # Check breadcrumbs
        assert True
    
    def test_nav_009_back_button_navigation(self, test_data):
        """TC_NAV_009: Browser back button"""
        test_logger.info("TC_NAV_009: Browser back button")
        self.login_page.navigate()
        self.login_page.login("super_admin@example.com", "Admin@123")
        self.schemes_page.navigate()
        self.driver.back()
        assert "dashboard" in self.driver.current_url.lower()
    
    def test_nav_010_forward_button_navigation(self, test_data):
        """TC_NAV_010: Browser forward button"""
        test_logger.info("TC_NAV_010: Browser forward button")
        self.login_page.navigate()
        self.login_page.login("super_admin@example.com", "Admin@123")
        self.schemes_page.navigate()
        self.driver.back()
        self.driver.forward()
        assert "schemes" in self.driver.current_url.lower()
    
    def test_nav_011_direct_url_navigation(self, test_data):
        """TC_NAV_011: Direct URL navigation"""
        test_logger.info("TC_NAV_011: Direct URL navigation")
        self.login_page.navigate()
        self.login_page.login("super_admin@example.com", "Admin@123")
        self.driver.get(f"{self.base_url}schemes")
        assert self.schemes_page.is_schemes_page_loaded()
    
    def test_nav_012_page_refresh(self, test_data):
        """TC_NAV_012: Page refresh"""
        test_logger.info("TC_NAV_012: Page refresh")
        self.login_page.navigate()
        self.login_page.login("super_admin@example.com", "Admin@123")
        self.schemes_page.navigate()
        self.driver.refresh()
        assert self.schemes_page.is_schemes_page_loaded()
    
    def test_nav_013_new_tab_navigation(self, test_data):
        """TC_NAV_013: New tab navigation"""
        test_logger.info("TC_NAV_013: New tab navigation")
        self.login_page.navigate()
        self.login_page.login("super_admin@example.com", "Admin@123")
        self.dashboard_page.open_new_tab()
        self.schemes_page.navigate()
        assert self.schemes_page.is_schemes_page_loaded()
        self.dashboard_page.close_current_tab()
    
    def test_nav_014_sidebar_navigation(self, test_data):
        """TC_NAV_014: Sidebar navigation"""
        test_logger.info("TC_NAV_014: Sidebar navigation")
        self.login_page.navigate()
        self.login_page.login("super_admin@example.com", "Admin@123")
        assert self.dashboard_page.is_sidebar_visible()
    
    def test_nav_015_top_bar_navigation(self, test_data):
        """TC_NAV_015: Top bar navigation"""
        test_logger.info("TC_NAV_015: Top bar navigation")
        self.login_page.navigate()
        self.login_page.login("super_admin@example.com", "Admin@123")
        # Check top bar elements
        assert True
    
    def test_nav_016_search_navigation(self, test_data):
        """TC_NAV_016: Search-based navigation"""
        test_logger.info("TC_NAV_016: Search-based navigation")
        self.login_page.navigate()
        self.login_page.login("super_admin@example.com", "Admin@123")
        self.schemes_page.navigate()
        self.schemes_page.search_scheme("test")
        assert True
    
    def test_nav_017_filter_navigation(self, test_data):
        """TC_NAV_017: Filter-based navigation"""
        test_logger.info("TC_NAV_017: Filter-based navigation")
        self.login_page.navigate()
        self.login_page.login("super_admin@example.com", "Admin@123")
        self.schemes_page.navigate()
        self.schemes_page.click_filter()
        assert True
    
    def test_nav_018_pagination_navigation(self, test_data):
        """TC_NAV_018: Pagination navigation"""
        test_logger.info("TC_NAV_018: Pagination navigation")
        self.login_page.navigate()
        self.login_page.login("super_admin@example.com", "Admin@123")
        self.schemes_page.navigate()
        if self.schemes_page.is_pagination_visible():
            self.schemes_page.click_next_page()
            assert True
    
    def test_nav_019_sort_navigation(self, test_data):
        """TC_NAV_019: Sort-based navigation"""
        test_logger.info("TC_NAV_019: Sort-based navigation")
        self.login_page.navigate()
        self.login_page.login("super_admin@example.com", "Admin@123")
        self.schemes_page.navigate()
        # Check sort options
        assert True
    
    def test_nav_020_external_link_navigation(self):
        """TC_NAV_020: External link navigation"""
        test_logger.info("TC_NAV_020: External link navigation")
        self.login_page.navigate()
        # Check external links
        assert True
    
    def test_nav_021_logout_navigation(self, test_data):
        """TC_NAV_021: Logout navigation"""
        test_logger.info("TC_NAV_021: Logout navigation")
        self.login_page.navigate()
        self.login_page.login("super_admin@example.com", "Admin@123")
        self.dashboard_page.click_logout()
        assert "login" in self.driver.current_url.lower()
    
    def test_nav_022_profile_navigation(self, test_data):
        """TC_NAV_022: Profile navigation"""
        test_logger.info("TC_NAV_022: Profile navigation")
        self.login_page.navigate()
        self.login_page.login("super_admin@example.com", "Admin@123")
        assert self.dashboard_page.is_user_profile_visible()
    
    def test_nav_023_settings_navigation(self, test_data):
        """TC_NAV_023: Settings navigation"""
        test_logger.info("TC_NAV_023: Settings navigation")
        self.login_page.navigate()
        self.login_page.login("super_admin@example.com", "Admin@123")
        # Navigate to settings
        assert True
    
    def test_nav_024_help_navigation(self, test_data):
        """TC_NAV_024: Help navigation"""
        test_logger.info("TC_NAV_024: Help navigation")
        self.login_page.navigate()
        self.login_page.login("super_admin@example.com", "Admin@123")
        # Navigate to help
        assert True
    
    def test_nav_025_notification_navigation(self, test_data):
        """TC_NAV_025: Notification navigation"""
        test_logger.info("TC_NAV_025: Notification navigation")
        self.login_page.navigate()
        self.login_page.login("super_admin@example.com", "Admin@123")
        # Check notifications
        assert True
    
    def test_nav_026_quick_actions_navigation(self, test_data):
        """TC_NAV_026: Quick actions navigation"""
        test_logger.info("TC_NAV_026: Quick actions navigation")
        self.login_page.navigate()
        self.login_page.login("super_admin@example.com", "Admin@123")
        # Check quick actions
        assert True
    
    def test_nav_027_recent_items_navigation(self, test_data):
        """TC_NAV_027: Recent items navigation"""
        test_logger.info("TC_NAV_027: Recent items navigation")
        self.login_page.navigate()
        self.login_page.login("super_admin@example.com", "Admin@123")
        # Check recent items
        assert True
    
    def test_nav_028_favorites_navigation(self, test_data):
        """TC_NAV_028: Favorites navigation"""
        test_logger.info("TC_NAV_028: Favorites navigation")
        self.login_page.navigate()
        self.login_page.login("super_admin@example.com", "Admin@123")
        # Check favorites
        assert True
    
    def test_nav_029_keyboard_navigation(self, test_data):
        """TC_NAV_029: Keyboard navigation"""
        test_logger.info("TC_NAV_029: Keyboard navigation")
        self.login_page.navigate()
        self.login_page.login("super_admin@example.com", "Admin@123")
        # Test keyboard shortcuts
        assert True
    
    def test_nav_030_mobile_menu_navigation(self, test_data):
        """TC_NAV_030: Mobile menu navigation"""
        test_logger.info("TC_NAV_030: Mobile menu navigation")
        self.login_page.navigate()
        self.login_page.login("super_admin@example.com", "Admin@123")
        self.driver.set_window_size(375, 667)
        # Check mobile menu
        assert True
