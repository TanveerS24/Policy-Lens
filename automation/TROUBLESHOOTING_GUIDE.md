# Troubleshooting Guide

This guide helps you troubleshoot common issues with the Selenium E2E test suite and CI/CD pipeline.

## Table of Contents

- [Local Execution Issues](#local-execution-issues)
- [CI/CD Pipeline Issues](#cicd-pipeline-issues)
- [Test Execution Issues](#test-execution-issues)
- [Deployment Issues](#deployment-issues)
- [Report Generation Issues](#report-generation-issues)
- [Browser/WebDriver Issues](#browserwebdriver-issues)

## Local Execution Issues

### Issue: Import Errors

**Symptom:** `ModuleNotFoundError: No module named 'config'`

**Solution:**
```bash
# Ensure you're in the automation directory
cd automation

# Add parent directory to Python path
export PYTHONPATH="${PYTHONPATH}:.."

# On Windows
set PYTHONPATH=%PYTHONPATH%;..
```

### Issue: WebDriver Not Found

**Symptom:** `WebDriverException: Message: 'chromedriver' executable needs to be in PATH`

**Solution:**
```bash
# Install webdriver-manager
pip install --upgrade webdriver-manager

# Or manually download ChromeDriver
# https://chromedriver.chromium.org/downloads
```

### Issue: Timeout Errors

**Symptom:** Tests timeout frequently

**Solution:**
```env
# Increase timeout values in .env
EXPLICIT_WAIT=60
PAGE_LOAD_TIMEOUT=120
```

### Issue: Headless Mode Issues

**Symptom:** Tests fail in headless mode but pass with visible browser

**Solution:**
```env
# Disable headless mode
HEADLESS=false
```

### Issue: BASE_URL Configuration

**Symptom:** Tests fail with connection refused

**Solution:**
```env
# Ensure BASE_URL is set correctly
# Never use localhost for CI/CD
BASE_URL=https://your-username.github.io/your-repo/
```

## CI/CD Pipeline Issues

### Issue: Pipeline Fails at Deployment Stage

**Symptom:** Deployment to GitHub Pages fails

**Solution:**
1. Check GitHub Pages settings in repository
2. Verify source branch is set correctly
3. Check build logs for specific errors
4. Ensure `GITHUB_TOKEN` has write permissions

### Issue: Deployment Verification Fails

**Symptom:** Deployment verification stage fails

**Solution:**
1. Check if GitHub Pages URL is accessible
2. Verify BASE_URL is constructed correctly
3. Increase wait time for deployment propagation
4. Check network connectivity in workflow

### Issue: Tests Fail in CI but Pass Locally

**Symptom:** Tests pass locally but fail in GitHub Actions

**Solution:**
1. Check BASE_URL in workflow (must be GitHub Pages URL)
2. Verify environment variables are set correctly
3. Check for timing issues (increase waits)
4. Review screenshots in artifacts
5. Check logs for specific error messages

### Issue: Artifacts Not Uploaded

**Symptom:** Artifacts not available after workflow run

**Solution:**
1. Check artifact retention settings
2. Verify artifact upload step is not skipped
3. Check workflow permissions for artifacts
4. Ensure artifact path is correct

### Issue: Workflow Permission Errors

**Symptom:** `Resource not accessible by integration`

**Solution:**
1. Go to repository Settings → Actions → General
2. Under "Workflow permissions", select "Read and write permissions"
3. Save changes

## Test Execution Issues

### Issue: Element Not Found

**Symptom:** `NoSuchElementException: Unable to locate element`

**Solution:**
1. Increase explicit wait time
2. Check element locator is correct
3. Verify element exists on page
4. Check if page is fully loaded
5. Review screenshot for page state

### Issue: Stale Element Reference

**Symptom:** `StaleElementReferenceException: stale element reference`

**Solution:**
1. Re-find element before interaction
2. Add wait for element to be refreshed
3. Use explicit waits instead of implicit
4. Check if page has changed dynamically

### Issue: Element Click Intercepted

**Symptom:** `ElementClickInterceptedException: Element click intercepted`

**Solution:**
1. Scroll element into view
2. Wait for element to be clickable
3. Check if overlay is blocking element
4. Use JavaScript click as fallback

### Issue: Timeout Waiting for Element

**Symptom:** `TimeoutException: Timed out waiting for element`

**Solution:**
1. Increase explicit wait timeout
2. Check if element exists on page
3. Verify page is fully loaded
4. Check for loading spinners or overlays

### Issue: Flaky Tests

**Symptom:** Tests pass/fail inconsistently

**Solution:**
1. Add retry logic: `--reruns 3`
2. Increase wait times
3. Use more robust locators
4. Add explicit waits
5. Check for race conditions

## Deployment Issues

### Issue: GitHub Pages Not Accessible

**Symptom:** GitHub Pages URL returns 404

**Solution:**
1. Check GitHub Pages is enabled
2. Verify source branch is correct
3. Wait for deployment to complete (up to 10 minutes)
4. Check repository settings for custom domain

### Issue: Wrong URL in Tests

**Symptom:** Tests run against wrong URL

**Solution:**
1. Check BASE_URL environment variable
2. Verify workflow URL construction
3. Ensure repository name is correct
4. Check for typos in URL

### Issue: Deployment Not Propagating

**Symptom:** Deployment verification fails due to propagation delay

**Solution:**
1. Increase wait time in workflow
2. Add retry logic for verification
3. Check GitHub Pages status page
4. Verify DNS propagation

## Report Generation Issues

### Issue: Excel Report Generation Fails

**Symptom:** `ImportError: No module named 'openpyxl'`

**Solution:**
```bash
pip install openpyxl xlsxwriter
```

### Issue: JSON Report Generation Fails

**Symptom:** JSON report file not created

**Solution:**
1. Check reports directory exists
2. Verify write permissions
3. Check for JSON serialization errors
4. Review script logs

### Issue: HTML Report Not Generated

**Symptom:**
 HTML report not created

**Solution:**
1. Install pytest-html: `pip install pytest-html`
2. Check reports directory exists
3. Verify HTML generation parameters
4. Check for template errors

## Browser/WebDriver Issues

### Issue: Chrome Version Mismatch

**Symptom:** `SessionNotCreatedException: Message: session not created: This version of ChromeDriver only supports Chrome version`

**Solution:**
```bash
# Update webdriver-manager
pip install --upgrade webdriver-manager

# Or manually update ChromeDriver
# https://chromedriver.chromium.org/downloads
```

### Issue: Browser Not Launching

**Symptom:** WebDriver fails to launch browser

**Solution:**
1. Check browser is installed
2. Verify browser version compatibility
3. Check for conflicting browser instances
4. Try different browser (Firefox, Edge)

### Issue: Headless Chrome Issues

**Symptom:** Tests fail in headless mode

**Solution:**
```python
# Add these Chrome options
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
```

### Issue: SSL Certificate Errors

**Symptom:** SSL certificate errors in headless mode

**Solution:**
```python
# Ignore SSL errors (for testing only)
options.add_argument("--ignore-certificate-errors")
options.add_argument("--allow-running-insecure-content")
```

## Getting Help

### Check Logs

1. **Local execution:** Check `automation/logs/`
2. **CI/CD:** Check GitHub Actions workflow logs
3. **Screenshots:** Check `automation/screenshots/`

### Review Artifacts

1. Download workflow artifacts
2. Review Excel reports for failure details
3. Check screenshots for visual issues
4. Review JSON for detailed results

### Common Debugging Steps

1. Run single test to isolate issue
2. Run with visible browser to see what's happening
3. Increase wait times to rule out timing issues
4. Check page source to verify elements exist
5. Use browser DevTools to inspect elements

### Report Issues

When reporting issues, include:

1. Error message and stack trace
2. Test case that failed
3. Screenshot of failure
4. Logs from execution
5. Environment details (OS, browser, Python version)
6. Steps to reproduce

## Prevention

### Best Practices

1. **Always test locally first** - Verify tests pass before pushing
2. **Use explicit waits** - Avoid hard-coded sleeps
3. **Robust locators** - Use stable, unique locators
4. **Regular updates** - Keep dependencies updated
5. **Monitor CI/CD** - Watch pipeline for issues
6. **Review artifacts** - Check results after each run

### Maintenance

1. Update test data regularly
2. Review and update locators as UI changes
3. Keep test data in sync with application
4. Regularly review and optimize tests
5. Update dependencies for security patches
