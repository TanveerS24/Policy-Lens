# Local Execution Guide

This guide provides instructions for running the Selenium E2E test suite locally.

## Prerequisites

- Python 3.11+
- Google Chrome browser
- Node.js 20+ (for building the application)

## Setup

### 1. Install Python Dependencies

```bash
cd automation
pip install -r requirements.txt
```

### 2. Set Environment Variables

Create a `.env` file in the `automation` directory:

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

**IMPORTANT:** Never use `localhost` or `127.0.0.1` as BASE_URL. Always use the LIVE deployment URL.

### 3. Build the Application

```bash
cd admin-frontend
npm install
npm run build
```

### 4. Serve the Application (Optional)

For local testing, you can serve the built application:

```bash
cd admin-frontend
npx serve dist -l 5173
```

Then set `BASE_URL=http://localhost:5173/` in your `.env` file.

## Running Tests

### Run All Tests

```bash
cd automation
python -m pytest tests/ -v
```

### Run Specific Test Categories

```bash
# Authentication tests
python -m pytest tests/test_authentication.py -v -m auth

# Authorization tests
python -m pytest tests/test_authorization.py -v -m authz

# Navigation tests
python -m pytest tests/test_navigation.py -v -m nav

# UI validation tests
python -m pytest tests/test_ui_validation.py -v -m ui

# Forms tests
python -m pytest tests/test_forms.py -v -m form

# CRUD operations tests
python -m pytest tests/test_crud_operations.py -v -m crud

# Input validation tests
python -m pytest tests/test_validation.py -v -m validation

# Error handling tests
python -m pytest tests/test_error_handling.py -v -m error

# Session management tests
python -m pytest tests/test_session_management.py -v -m session

# File upload tests
python -m pytest tests/test_file_upload.py -v -m upload

# Accessibility tests
python -m pytest tests/test_accessibility.py -v -m a11y

# Responsive design tests
python -m pytest tests/test_responsive_design.py -v -m responsive

# Performance tests
python -m pytest tests/test_performance.py -v -m performance

# Regression tests
python -m pytest tests/test_regression.py -v -m regression
```

### Run Tests in Parallel

```bash
python -m pytest tests/ -v -n 4
```

### Run Tests with HTML Report

```bash
python -m pytest tests/ -v --html=reports/execution-report.html --self-contained-html
```

### Run Tests with Retry

```bash
python -m pytest tests/ -v --reruns 3
```

### Run Specific Test

```bash
python -m pytest tests/test_authentication.py::TestAuthentication::test_auth_001 -v
```

## Generating Reports

### Generate All Reports

```bash
cd automation
python utils/generate_json_report.py
python utils/generate_excel_report.py
python utils/generate_summary_report.py
```

### Generate JSON Report Only

```bash
python utils/generate_json_report.py
```

### Generate Excel Report Only

```bash
python utils/generate_excel_report.py
```

### Generate Summary Report Only

```bash
python utils/generate_summary_report.py
```

## Viewing Reports

### HTML Report

Open `automation/reports/execution-report.html` in your browser.

### Excel Reports

- `automation/Automation_Test_Report.xlsx` - Complete test report
- `automation/Passed_Test_Cases.xlsx` - Passed tests only
- `automation/Failed_Test_Cases.xlsx` - Failed tests only
- `automation/Summary_Report.xlsx` - Summary metrics

### JSON Report

Open `automation/reports/execution-results.json` in any JSON viewer.

### Screenshots

Screenshots are saved in `automation/screenshots/`

### Logs

Logs are saved in `automation/logs/`

## Troubleshooting

### WebDriver Issues

If you encounter WebDriver issues:

```bash
# Update ChromeDriver
pip install --upgrade webdriver-manager
```

### Import Errors

If you encounter import errors:

```bash
# Ensure you're in the automation directory
cd automation

# Add parent directory to Python path
export PYTHONPATH="${PYTHONPATH}:.."
```

### Timeout Errors

If tests timeout frequently, increase timeout values in `.env`:

```env
EXPLICIT_WAIT=60
PAGE_LOAD_TIMEOUT=120
```

### Headless Mode Issues

If headless mode causes issues, run with visible browser:

```env
HEADLESS=false
```

## Best Practices

1. **Always use LIVE deployment URL** - Never test against localhost in CI/CD
2. **Clean up before running** - Clear old reports and screenshots
3. **Use specific markers** - Run specific test categories when debugging
4. **Check logs** - Review logs in `automation/logs/` for detailed information
5. **Review screenshots** - Check screenshots for failed tests
6. **Parallel execution** - Use parallel execution for faster test runs
7. **Environment variables** - Keep sensitive data in environment variables

## Test Data

Test data is managed in `automation/data/test_data.json`. Modify this file to update test data.

## Continuous Integration

The local execution setup mirrors the CI/CD pipeline. Ensure local tests pass before pushing to trigger the pipeline.
