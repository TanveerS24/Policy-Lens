# Selenium E2E Automation Framework

Enterprise-grade Selenium automation framework for Policy-Lens application with complete CI/CD integration.

## Overview

This framework provides comprehensive end-to-end testing for the Policy-Lens application with:
- **400+ test cases** across 13 categories
- **Page Object Model** architecture
- **Parallel test execution** support
- **Comprehensive reporting** (Excel, HTML, JSON)
- **CI/CD integration** with GitHub Actions
- **Deployment verification** against LIVE GitHub Pages
- **Screenshot capture** on failures
- **Detailed logging** with loguru
- **Test data management** framework

## Test Categories

| Category | Test Cases | Description |
|----------|------------|-------------|
| Authentication | 40 | Login, logout, session management |
| Authorization | 40 | Role-based access control |
| Navigation | 30 | Page navigation and routing |
| UI Validation | 50 | UI elements and layout validation |
| Forms | 50 | Form submission and validation |
| CRUD Operations | 50 | Create, Read, Update, Delete operations |
| Input Validation | 40 | Field validation and sanitization |
| Error Handling | 20 | Error message and exception handling |
| Session Management | 20 | Session lifecycle and security |
| File Upload | 20 | File upload functionality |
| Accessibility | 20 | A11y and screen reader compatibility |
| Responsive Design | 20 | Mobile and tablet responsiveness |
| Performance | 20 | Load time and response time testing |
| Regression | 50 | Comprehensive regression suite |

**Total: 400+ test cases**

## Project Structure

```
automation/
├── config/
│   ├── __init__.py
│   └── config.py              # Configuration management
├── pages/
│   ├── __init__.py
│   ├── base_page.py           # Base page class
│   ├── login_page.py          # Login page object
│   ├── dashboard_page.py      # Dashboard page object
│   ├── schemes_page.py        # Schemes page object
│   ├── users_page.py          # Users page object
│   └── admins_page.py         # Admins page object
├── tests/
│   ├── __init__.py
│   ├── conftest.py            # Pytest configuration
│   ├── test_authentication.py  # Authentication tests (40)
│   ├── test_authorization.py  # Authorization tests (40)
│   ├── test_navigation.py     # Navigation tests (30)
│   ├── test_ui_validation.py  # UI validation tests (50)
│   ├── test_forms.py          # Forms tests (50)
│   ├── test_crud_operations.py # CRUD tests (50)
│   ├── test_validation.py     # Input validation tests (40)
│   ├── test_error_handling.py # Error handling tests (20)
│   ├── test_session_management.py # Session tests (20)
│   ├── test_file_upload.py    # File upload tests (20)
│   ├── test_accessibility.py  # Accessibility tests (20)
│   ├── test_responsive_design.py # Responsive tests (20)
│   ├── test_performance.py    # Performance tests (20)
│   └── test_regression.py     # Regression tests (50)
├── utils/
│   ├── __init__.py
│   ├── logger.py              # Logging utilities
│   ├── screenshot.py          # Screenshot capture
│   ├── driver_factory.py      # WebDriver factory
│   ├── wait_helper.py         # Explicit wait helpers
│   ├── generate_json_report.py    # JSON report generator
│   ├── generate_excel_report.py   # Excel report generator
│   ├── generate_summary_report.py # Summary generator
│   └── verify_deployment.py  # Deployment verification
├── data/
│   ├── __init__.py
│   └── test_data.json        # Test data management
├── reports/                   # Test reports directory
├── screenshots/               # Screenshots directory
├── logs/                      # Log files directory
├── history/                   # Historical results
├── drivers/                   # WebDriver storage
├── requirements.txt           # Python dependencies
├── conftest.py               # Pytest fixtures
├── LOCAL_EXECUTION_GUIDE.md   # Local execution guide
├── CI_CD_EXECUTION_GUIDE.md  # CI/CD guide
├── TROUBLESHOOTING_GUIDE.md  # Troubleshooting guide
└── GITHUB_REPOSITORY_CONFIGURATION.md # GitHub setup guide
```

## Quick Start

### Prerequisites

- Python 3.11+
- Google Chrome browser
- Node.js 20+ (for building application)

### Installation

```bash
cd automation
pip install -r requirements.txt
```

### Configuration

Create `.env` file:

```env
BASE_URL=https://your-username.github.io/your-repo/
BROWSER=chrome
HEADLESS=false
IMPLICIT_WAIT=10
EXPLICIT_WAIT=30
PAGE_LOAD_TIMEOUT=60
LOG_LEVEL=INFO
PARALLEL_EXECUTION=true
WORKERS=4
MIN_PASS_PERCENTAGE=90.0
```

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific category
python -m pytest tests/test_authentication.py -v -m auth

# Run in parallel
python -m pytest tests/ -v -n 4

# Run with HTML report
python -m pytest tests/ -v --html=reports/execution-report.html --self-contained-html
```

## CI/CD Pipeline

The framework integrates with GitHub Actions for automated testing:

### Pipeline Stages

1. Repository Checkout
2. Dependency Installation
3. Build Application
4. Static Analysis
5. Deploy to GitHub Pages
6. Wait for Deployment
7. Deployment Verification
8. Run Selenium E2E Tests
9. Generate Reports
10. Generate Excel Reports
11. Upload Artifacts
12. Publish Summary
13. Store Historical Results

### Triggers

- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`
- Manual workflow dispatch

### Artifacts

All test execution artifacts are uploaded:
- Excel reports (Automation_Test_Report.xlsx, Passed_Test_Cases.xlsx, Failed_Test_Cases.xlsx, Summary_Report.xlsx)
- HTML reports (execution-report.html)
- Screenshots
- Logs
- JSON results
- Summary markdown

## Reporting

### Excel Reports

- **Automation_Test_Report.xlsx** - Complete report with 6 sheets
  - Executed Test Cases
  - Passed Tests
  - Failed Tests
  - Skipped Tests
  - Execution Metrics
  - Defect Summary

- **Passed_Test_Cases.xlsx** - Passed tests only
- **Failed_Test_Cases.xlsx** - Failed tests with failure reasons
- **Summary_Report.xlsx** - Summary metrics

### HTML Report

Interactive HTML report with:
- Test execution summary
- Pass/fail statistics
- Module-wise breakdown
- Failure details
- Screenshots

### JSON Report

Machine-readable JSON report with:
- Execution summary
- Test results
- Module statistics
- Environment details

## Key Features

### Page Object Model

Clean separation of test logic and page interactions:

```python
from pages.login_page import LoginPage

login_page = LoginPage(driver)
login_page.navigate()
login_page.login("admin@example.com", "password")
```

### Explicit Waits

Robust waiting with custom wait helper:

```python
from utils.wait_helper import WaitHelper

wait_helper = WaitHelper(driver)
wait_helper.wait_for_element_visible(locator)
wait_helper.wait_for_element_clickable(locator)
```

### Screenshot Capture

Automatic screenshot capture on failures:

```python
from utils.screenshot import ScreenshotManager

screenshot_manager = ScreenshotManager(driver)
screenshot_manager.capture_on_failure(test_name, error_message)
```

### Logging

Comprehensive logging with loguru:

```python
from utils.logger import test_logger

test_logger.info("Test execution started")
test_logger.error("Test failed with error")
```

### Test Data Management

Centralized test data management:

```python
from data import test_data_manager

user_data = test_data_manager.get_user("super_admin")
valid_emails = test_data_manager.get_valid_emails()
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| BASE_URL | Application URL | Required |
| BROWSER | Browser type | chrome |
| HEADLESS | Headless mode | true |
| IMPLICIT_WAIT | Implicit wait (seconds) | 10 |
| EXPLICIT_WAIT | Explicit wait (seconds) | 30 |
| PAGE_LOAD_TIMEOUT | Page load timeout (seconds) | 60 |
| LOG_LEVEL | Logging level | INFO |
| PARALLEL_EXECUTION | Parallel execution | true |
| WORKERS | Number of parallel workers | 4 |
| MIN_PASS_PERCENTAGE | Minimum pass percentage | 90.0 |

### Pass/Fail Criteria

**Workflow Fails If:**
- Deployment verification fails
- More than 5% critical test cases fail

**Workflow Succeeds If:**
- Deployment verification succeeds
- Pass percentage ≥ 95%

## Documentation

- [LOCAL_EXECUTION_GUIDE.md](LOCAL_EXECUTION_GUIDE.md) - Local execution instructions
- [CI_CD_EXECUTION_GUIDE.md](CI_CD_EXECUTION_GUIDE.md) - CI/CD pipeline guide
- [TROUBLESHOOTING_GUIDE.md](TROUBLESHOOTING_GUIDE.md) - Troubleshooting common issues
- [GITHUB_REPOSITORY_CONFIGURATION.md](GITHUB_REPOSITORY_CONFIGURATION.md) - GitHub setup instructions

## Best Practices

1. **Always use LIVE deployment URL** - Never test against localhost in CI/CD
2. **Use Page Object Model** - Maintain clean test architecture
3. **Explicit waits over sleeps** - Use explicit waits for reliability
4. **Parallel execution** - Use parallel execution for faster runs
5. **Review artifacts** - Check screenshots and logs for failures
6. **Keep test data updated** - Maintain test data in JSON files
7. **Run locally first** - Verify tests pass before pushing

## Maintenance

### Updating Test Cases

1. Add new test methods to appropriate test files
2. Use descriptive test names with TC_ prefix
3. Add appropriate markers (@pytest.mark.category)
4. Update test data if needed

### Updating Page Objects

1. Add new page classes to `pages/` directory
2. Inherit from `BasePage`
3. Define locators as class constants
4. Implement page-specific methods

### Adding New Test Categories

1. Create new test file in `tests/`
2. Add marker in `conftest.py`
3. Update documentation
4. Add to test count summary

## Support

For issues and questions:
1. Check [TROUBLESHOOTING_GUIDE.md](TROUBLESHOOTING_GUIDE.md)
2. Review logs in `logs/` directory
3. Check screenshots in `screenshots/` directory
4. Review GitHub Actions workflow logs

## License

This framework is part of the Policy-Lens project.
