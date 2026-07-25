"""
Pytest configuration and fixtures
"""

import pytest
import os
import sys
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import config
from utils.driver_factory import DriverFactory
from utils.logger import test_logger
from utils.screenshot import ScreenshotManager


@pytest.fixture(scope="function")
def driver():
    """
    Fixture to provide WebDriver instance for each test
    """
    driver = None
    try:
        driver = DriverFactory.get_driver()
        driver.maximize_window()
        yield driver
    finally:
        if driver:
            DriverFactory.quit_driver(driver)


@pytest.fixture(scope="function")
def base_url():
    """
    Fixture to provide base URL
    """
    return config.BASE_URL


@pytest.fixture(scope="function")
def screenshot_manager(driver):
    """
    Fixture to provide screenshot manager
    """
    return ScreenshotManager(driver)


@pytest.fixture(scope="session")
def test_run_id():
    """
    Fixture to provide unique test run ID
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S")


@pytest.fixture(scope="function", autouse=True)
def test_logging(request):
    """
    Fixture to log test start and end
    """
    test_name = request.node.name
    test_logger.test_start(test_name)
    start_time = datetime.now()
    
    yield
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    status = "passed" if request.node.rep_call.passed else "failed"
    test_logger.test_end(test_name, status, duration)


@pytest.fixture(scope="function")
def test_data():
    """
    Fixture to provide test data
    """
    return {
        "valid_email": "test@example.com",
        "invalid_email": "invalid-email",
        "valid_password": "Test@123456",
        "short_password": "Test1",
        "long_password": "T" * 101,
        "admin_email": "admin@example.com",
        "admin_password": "Admin@123456",
        "scheme_name": "Test Scheme",
        "scheme_description": "Test scheme description",
        "user_name": "Test User",
        "user_phone": "1234567890",
    }


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test execution status
    """
    outcome = yield
    rep = outcome.get_result()
    
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(scope="function")
def on_failure_screenshot(request, driver, screenshot_manager):
    """
    Fixture to capture screenshot on test failure
    """
    yield
    
    if request.node.rep_call.failed:
        test_name = request.node.name
        screenshot_manager.capture_on_failure(test_name)


def pytest_configure(config):
    """
    Pytest configuration hook
    """
    config.addinivalue_line(
        "markers", "auth: Authentication tests"
    )
    config.addinivalue_line(
        "markers", "authz: Authorization tests"
    )
    config.addinivalue_line(
        "markers", "nav: Navigation tests"
    )
    config.addinivalue_line(
        "markers", "ui: UI validation tests"
    )
    config.addinivalue_line(
        "markers", "form: Form tests"
    )
    config.addinivalue_line(
        "markers", "crud: CRUD operation tests"
    )
    config.addinivalue_line(
        "markers", "validation: Input validation tests"
    )
    config.addinivalue_line(
        "markers", "error: Error handling tests"
    )
    config.addinivalue_line(
        "markers", "session: Session management tests"
    )
    config.addinivalue_line(
        "markers", "upload: File upload tests"
    )
    config.addinivalue_line(
        "markers", "a11y: Accessibility tests"
    )
    config.addinivalue_line(
        "markers", "responsive: Responsive design tests"
    )
    config.addinivalue_line(
        "markers", "performance: Performance smoke tests"
    )
    config.addinivalue_line(
        "markers", "regression: Regression tests"
    )
    config.addinivalue_line(
        "markers", "api: API integration tests"
    )

