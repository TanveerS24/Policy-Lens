# CI/CD Execution Guide

This guide explains how the CI/CD pipeline works and how to monitor its execution.

## Pipeline Overview

The CI/CD pipeline is defined in `.github/workflows/deploy-and-test.yml` and consists of 13 stages:

1. **Repository Checkout** - Clones the repository
2. **Dependency Installation** - Installs Node.js and Python dependencies
3. **Build Application** - Builds the admin frontend
4. **Static Analysis** - Runs ESLint
5. **Deploy to GitHub Pages** - Deploys to GitHub Pages
6. **Wait for Deployment** - Waits for GitHub Pages to propagate
7. **Deployment Verification** - Verifies deployment is accessible
8. **Run Selenium E2E Tests** - Executes 400+ test cases against LIVE deployment
9. **Generate Reports** - Generates JSON and summary reports
10. **Generate Excel Reports** - Generates Excel reports with multiple sheets
11. **Upload Artifacts** - Uploads all reports as GitHub Actions artifacts
12. **Publish Summary** - Publishes execution summary to GitHub Actions
13. **Store Historical Results** - Stores historical test results

## Triggers

The pipeline is triggered on:

- **Push** to `main` or `develop` branches
- **Pull Request** to `main` or `develop` branches
- **Manual Dispatch** via GitHub Actions UI

## Execution Flow

### 1. Build and Deploy

```yaml
- Build admin frontend
- Deploy to GitHub Pages
- Wait 60 seconds for propagation
```

### 2. Deployment Verification

```yaml
- Check HTTP status (must be 200)
- Verify HTML structure
- Check critical assets
- Mark deployment as success/failure
```

### 3. Test Execution

```yaml
- Set BASE_URL to GitHub Pages URL
- Run 400+ Selenium tests in parallel (4 workers)
- Capture screenshots on failure
- Generate execution reports
```

### 4. Report Generation

```yaml
- Generate JSON report
- Generate Excel reports (6 sheets)
- Generate summary markdown
- Upload all artifacts
- Publish GitHub Actions summary
```

## Monitoring Execution

### View Pipeline Status

1. Go to your repository on GitHub
2. Click on "Actions" tab
3. Select the "Deploy and Test" workflow
4. View the latest run

### View Logs

1. Click on the workflow run
2. Expand each job to view logs
3. Check for errors in each stage

### Download Artifacts

1. Click on the workflow run
2. Scroll to "Artifacts" section
3. Download:
   - `test-reports` - Complete report package
   - Contains Excel, HTML, JSON, screenshots, and logs

### View Summary

The execution summary is automatically published at the bottom of the workflow run page.

## Deployment URL

The deployment URL is automatically constructed:

```
https://<github-username>.github.io/<repository-name>/
```

This is set via the `BASE_URL` environment variable in the workflow.

## Pass/Fail Criteria

### Workflow Fails If:

- Deployment verification fails
- More than 5% critical test cases fail

### Workflow Succeeds If:

- Deployment verification succeeds
- Pass percentage ≥ 95%

## Environment Variables

The workflow uses the following environment variables:

```yaml
BASE_URL: https://${{ github.repository_owner }}.github.io/${{ github.event.repository.name }}/
PYTHON_VERSION: '3.11'
NODE_VERSION: '20'
```

## Parallel Execution

Tests run in parallel using pytest-xdist with 4 workers:

```yaml
python -m pytest tests/ -n 4
```

This significantly reduces execution time.

## Artifact Retention

All artifacts are retained for 30 days:

- Excel reports
- HTML reports
- Screenshots
- Logs
- JSON results
- Summary markdown

## Historical Results

Historical test results are stored in `automation/history/` with timestamps:

```
automation/history/
├── reports_20240125_143022/
├── screenshots_20240125_143022/
└── execution-results_20240125_143022.json
```

Only the last 10 executions are retained.

## Manual Execution

You can manually trigger the pipeline:

1. Go to repository → Actions
2. Select "Deploy and Test" workflow
3. Click "Run workflow"
4. Select branch
5. Click "Run workflow" button

## Troubleshooting Pipeline Issues

### Deployment Fails

- Check GitHub Pages settings
- Verify branch configuration
- Check build logs

### Tests Fail

- Download artifacts
- Review failed test screenshots
- Check logs for error details
- Verify BASE_URL is correct

### Timeout Errors

- Increase wait times in workflow
- Check network connectivity
- Verify GitHub Pages is accessible

### Permission Errors

- Check repository permissions
- Verify GitHub Actions is enabled
- Check workflow permissions

## Best Practices

1. **Test locally first** - Ensure tests pass locally before pushing
2. **Monitor execution** - Watch pipeline execution for issues
3. **Review artifacts** - Download and review artifacts after each run
4. **Check summaries** - Review GitHub Actions summary for quick overview
5. **Keep dependencies updated** - Regularly update dependencies
6. **Use feature branches** - Test on feature branches before merging to main

## Integration with Development Workflow

### Feature Branch Workflow

1. Create feature branch
2. Make changes
3. Push to feature branch
4. Pipeline runs automatically
5. Review results
6. Fix any issues
7. Create pull request
8. Pipeline runs on PR
9. Merge to main
10. Pipeline runs on main (deploys to production)

### Hotfix Workflow

1. Create hotfix branch from main
2. Make urgent fix
3. Push to hotfix branch
4. Pipeline runs automatically
5. Review results
6. Merge to main
7. Pipeline deploys to production immediately

## Security Considerations

- No secrets are hardcoded
- GitHub token is provided automatically
- BASE_URL is constructed from repository metadata
- All sensitive data uses GitHub Secrets

## Performance Optimization

- Parallel test execution (4 workers)
- Dependency caching
- Artifact compression
- Selective test execution using markers
- Retry logic for flaky tests
