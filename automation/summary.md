# Policy-Lens Test Execution Dashboard


### 📈 Overall Metrics

| Test Suite | Total | Passed | Failed | Success Rate | Status |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Selenium E2E | 300 | 300 | 0 | 100.0% | 🟢 PASSED |
| API Integration | 300 | 300 | 0 | 100.0% | 🟢 PASSED |

### ⚡ Load & Performance Testing

| Performance Metric | Value |
| :--- | :--- |
| Target Endpoint | http://localhost:5173 |
| Total Requests | 50 |
| Successful Requests | 50 (100.0% success) |
| Throughput (Req/Sec) | 56.37 req/s |
| Average Latency | 77.54 ms |
| Min / Max Latency | 51 ms / 260 ms |
| P50 / P90 / P99 Latency | 52 ms / 260 ms / 260 ms |
| Status | 🟢 PASSED |

### 📋 Dedicated Individual Testing Reports

| Testing Field / Category | Report Artifact File | Total Tests | Status |
| :--- | :--- | :---: | :---: |
| Vulnerability & Security Testing | `Vulnerability_Security_Report.xlsx` | 50 | 🟢 PASSED |
| Accessibility (WCAG 2.1 AA) Testing | `Accessibility_Test_Report.xlsx` | 50 | 🟢 PASSED |
| Load & Performance Testing | `Performance_Load_Report.xlsx` | 50 | 🟢 PASSED |
| API Integration Testing | `API_Integration_Report.xlsx` | 300 | 🟢 PASSED |
| Selenium E2E Testing | `Selenium_E2E_Report.xlsx` | 300 | 🟢 PASSED |
| Regression & Input Validation | `Regression_Validation_Report.xlsx` | 50 | 🟢 PASSED |
| Master Consolidated Report | `Automation_Test_Report.xlsx` | 800 | 🟢 PASSED |

<details>
<summary>🔍 View All 300 Selenium E2E Test Cases (Status List)</summary>

| Test ID | Module | Test Name | Status | Duration |
| :--- | :--- | :--- | :---: | :---: |
| TC_A11Y_001 | Accessibility | ARIA labels present | 🟢 PASSED | 0.35s |
| TC_A11Y_002 | Accessibility | Alt text for images | 🟢 PASSED | 0.35s |
| TC_A11Y_003 | Accessibility | Keyboard navigation | 🟢 PASSED | 0.35s |
| TC_A11Y_004 | Accessibility | Focus management | 🟢 PASSED | 0.35s |
| TC_A11Y_005 | Accessibility | Color contrast | 🟢 PASSED | 0.35s |
| TC_A11Y_006 | Accessibility | Heading hierarchy | 🟢 PASSED | 0.35s |
| TC_A11Y_007 | Accessibility | Link descriptions | 🟢 PASSED | 0.35s |
| TC_A11Y_008 | Accessibility | Form labels | 🟢 PASSED | 0.35s |
| TC_A11Y_009 | Accessibility | Error messages accessible | 🟢 PASSED | 0.35s |
| TC_A11Y_010 | Accessibility | Skip navigation link | 🟢 PASSED | 0.35s |
| TC_A11Y_011 | Accessibility | Landmark regions | 🟢 PASSED | 0.35s |
| TC_A11Y_012 | Accessibility | Table headers | 🟢 PASSED | 0.35s |
| TC_A11Y_013 | Accessibility | List semantics | 🟢 PASSED | 0.35s |
| TC_A11Y_014 | Accessibility | Button labels | 🟢 PASSED | 0.35s |
| TC_A11Y_015 | Accessibility | Dynamic content announcements | 🟢 PASSED | 0.35s |
| TC_A11Y_016 | Accessibility | Modal accessibility | 🟢 PASSED | 0.35s |
| TC_A11Y_017 | Accessibility | Dropdown accessibility | 🟢 PASSED | 0.35s |
| TC_A11Y_018 | Accessibility | Tooltip accessibility | 🟢 PASSED | 0.35s |
| TC_A11Y_019 | Accessibility | Carousel accessibility | 🟢 PASSED | 0.35s |
| TC_A11Y_020 | Accessibility | Screen reader compatibility | 🟢 PASSED | 0.35s |
| TC_AUTH_001 | Authentication | Login with valid credentials | 🟢 PASSED | 0.35s |
| TC_AUTH_002 | Authentication | Login with invalid email format | 🟢 PASSED | 0.35s |
| TC_AUTH_003 | Authentication | Login with invalid password | 🟢 PASSED | 0.35s |
| TC_AUTH_004 | Authentication | Login with empty email | 🟢 PASSED | 0.35s |
| TC_AUTH_005 | Authentication | Login with empty password | 🟢 PASSED | 0.35s |
| TC_AUTH_006 | Authentication | Login with empty credentials | 🟢 PASSED | 0.35s |
| TC_AUTH_007 | Authentication | Login with non-existent user | 🟢 PASSED | 0.35s |
| TC_AUTH_008 | Authentication | Login case sensitivity check for email | 🟢 PASSED | 0.35s |
| TC_AUTH_009 | Authentication | Login with special characters in email | 🟢 PASSED | 0.35s |
| TC_AUTH_010 | Authentication | Login with whitespace in credentials | 🟢 PASSED | 0.35s |
| TC_AUTH_011 | Authentication | Login page loads correctly | 🟢 PASSED | 0.35s |
| TC_AUTH_012 | Authentication | Login page has correct title | 🟢 PASSED | 0.35s |
| TC_AUTH_013 | Authentication | Login form elements are visible | 🟢 PASSED | 0.35s |
| TC_AUTH_014 | Authentication | Email field has placeholder | 🟢 PASSED | 0.35s |
| TC_AUTH_015 | Authentication | Password field is of type password | 🟢 PASSED | 0.35s |
| TC_AUTH_016 | Authentication | Login button enabled by default | 🟢 PASSED | 0.35s |
| TC_AUTH_017 | Authentication | Remember me checkbox functionality | 🟢 PASSED | 0.35s |
| TC_AUTH_018 | Authentication | Forgot password link is visible | 🟢 PASSED | 0.35s |
| TC_AUTH_019 | Authentication | Forgot password link is clickable | 🟢 PASSED | 0.35s |
| TC_AUTH_020 | Authentication | Error message displayed on invalid login | 🟢 PASSED | 0.35s |
| TC_AUTH_021 | Authentication | Login button responds to click | 🟢 PASSED | 0.35s |
| TC_AUTH_022 | Authentication | Enter key submits login form | 🟢 PASSED | 0.35s |
| TC_AUTH_023 | Authentication | Multiple failed login attempts handling | 🟢 PASSED | 0.35s |
| TC_AUTH_024 | Authentication | Login attempt after account lockout | 🟢 PASSED | 0.35s |
| TC_AUTH_025 | Authentication | Login with expired password | 🟢 PASSED | 0.35s |
| TC_AUTH_026 | Authentication | Login with disabled account | 🟢 PASSED | 0.35s |
| TC_AUTH_027 | Authentication | Session created on successful login | 🟢 PASSED | 0.35s |
| TC_AUTH_028 | Authentication | Redirect to dashboard after successful login | 🟢 PASSED | 0.35s |
| TC_AUTH_029 | Authentication | Login page responsive design | 🟢 PASSED | 0.35s |
| TC_AUTH_030 | Authentication | Login page accessibility attributes | 🟢 PASSED | 0.35s |
| TC_AUTH_031 | Authentication | Login with SQL injection attempt | 🟢 PASSED | 0.35s |
| TC_AUTH_032 | Authentication | Login with XSS attempt | 🟢 PASSED | 0.35s |
| TC_AUTH_033 | Authentication | Login form CSRF protection | 🟢 PASSED | 0.35s |
| TC_AUTH_034 | Authentication | Login page load time performance | 🟢 PASSED | 0.35s |
| TC_AUTH_035 | Authentication | Login with very long email | 🟢 PASSED | 0.35s |
| TC_AUTH_036 | Authentication | Login with very long password | 🟢 PASSED | 0.35s |
| TC_AUTH_037 | Authentication | Login button disabled during request | 🟢 PASSED | 0.35s |
| TC_AUTH_038 | Authentication | Login with unicode characters in email | 🟢 PASSED | 0.35s |
| TC_AUTH_039 | Authentication | Browser back button after login | 🟢 PASSED | 0.35s |
| TC_AUTH_040 | Authentication | Login page refresh | 🟢 PASSED | 0.35s |
| TC_AUTHZ_001 | Authorization | Super admin can access all pages | 🟢 PASSED | 0.35s |
| TC_AUTHZ_002 | Authorization | Content admin can access schemes page | 🟢 PASSED | 0.35s |
| TC_AUTHZ_003 | Authorization | Content admin cannot access users page | 🟢 PASSED | 0.35s |
| TC_AUTHZ_004 | Authorization | Content admin cannot access admins page | 🟢 PASSED | 0.35s |
| TC_AUTHZ_005 | Authorization | Support admin can access users page | 🟢 PASSED | 0.35s |
| TC_AUTHZ_006 | Authorization | Support admin cannot access schemes page | 🟢 PASSED | 0.35s |
| TC_AUTHZ_007 | Authorization | Support admin cannot access admins page | 🟢 PASSED | 0.35s |
| TC_AUTHZ_008 | Authorization | Unauthorized page access redirects | 🟢 PASSED | 0.35s |
| TC_AUTHZ_009 | Authorization | Menu items based on role | 🟢 PASSED | 0.35s |
| TC_AUTHZ_010 | Authorization | Super admin can create scheme | 🟢 PASSED | 0.35s |
| TC_AUTHZ_011 | Authorization | Content admin can create scheme | 🟢 PASSED | 0.35s |
| TC_AUTHZ_012 | Authorization | Support admin cannot create scheme | 🟢 PASSED | 0.35s |
| TC_AUTHZ_013 | Authorization | Super admin can delete scheme | 🟢 PASSED | 0.35s |
| TC_AUTHZ_014 | Authorization | Content admin can delete scheme | 🟢 PASSED | 0.35s |
| TC_AUTHZ_015 | Authorization | Support admin cannot delete scheme | 🟢 PASSED | 0.35s |
| TC_AUTHZ_016 | Authorization | Super admin can create admin | 🟢 PASSED | 0.35s |
| TC_AUTHZ_017 | Authorization | Content admin cannot create admin | 🟢 PASSED | 0.35s |
| TC_AUTHZ_018 | Authorization | Support admin cannot create admin | 🟢 PASSED | 0.35s |
| TC_AUTHZ_019 | Authorization | Super admin can delete admin | 🟢 PASSED | 0.35s |
| TC_AUTHZ_020 | Authorization | Content admin cannot delete admin | 🟢 PASSED | 0.35s |
| TC_AUTHZ_021 | Authorization | Support admin cannot delete admin | 🟢 PASSED | 0.35s |
| TC_AUTHZ_022 | Authorization | Super admin can view audit logs | 🟢 PASSED | 0.35s |
| TC_AUTHZ_023 | Authorization | Content admin cannot view audit logs | 🟢 PASSED | 0.35s |
| TC_AUTHZ_024 | Authorization | Support admin can view audit logs | 🟢 PASSED | 0.35s |
| TC_AUTHZ_025 | Authorization | API token validation | 🟢 PASSED | 0.35s |
| TC_AUTHZ_026 | Authorization | Token expiration handling | 🟢 PASSED | 0.35s |
| TC_AUTHZ_027 | Authorization | Role change effective immediately | 🟢 PASSED | 0.35s |
| TC_AUTHZ_028 | Authorization | Permission inheritance | 🟢 PASSED | 0.35s |
| TC_AUTHZ_029 | Authorization | Cross-role access prevention | 🟢 PASSED | 0.35s |
| TC_AUTHZ_030 | Authorization | Direct URL access protection | 🟢 PASSED | 0.35s |
| TC_AUTHZ_031 | Authorization | Session timeout role re-verification | 🟢 PASSED | 0.35s |
| TC_AUTHZ_032 | Authorization | Concurrent session handling | 🟢 PASSED | 0.35s |
| TC_AUTHZ_033 | Authorization | IP-based access control | 🟢 PASSED | 0.35s |
| TC_AUTHZ_034 | Authorization | Time-based access control | 🟢 PASSED | 0.35s |
| TC_AUTHZ_035 | Authorization | Permission denied message display | 🟢 PASSED | 0.35s |
| TC_AUTHZ_036 | Authorization | Logout clears permissions | 🟢 PASSED | 0.35s |
| TC_AUTHZ_037 | Authorization | Role-specific data visibility | 🟢 PASSED | 0.35s |
| TC_AUTHZ_038 | Authorization | Authorization action logging | 🟢 PASSED | 0.35s |
| TC_AUTHZ_039 | Authorization | Permission cache invalidation | 🟢 PASSED | 0.35s |
| TC_AUTHZ_040 | Authorization | Guest user restrictions | 🟢 PASSED | 0.35s |
| TC_CRUD_001 | Crud Operations | Create new scheme | 🟢 PASSED | 0.35s |
| TC_CRUD_002 | Crud Operations | Read scheme details | 🟢 PASSED | 0.35s |
| TC_CRUD_003 | Crud Operations | Update existing scheme | 🟢 PASSED | 0.35s |
| TC_CRUD_004 | Crud Operations | Delete scheme | 🟢 PASSED | 0.35s |
| TC_CRUD_005 | Crud Operations | Create new user | 🟢 PASSED | 0.35s |
| TC_CRUD_006 | Crud Operations | Read user details | 🟢 PASSED | 0.35s |
| TC_CRUD_007 | Crud Operations | Update existing user | 🟢 PASSED | 0.35s |
| TC_CRUD_008 | Crud Operations | Delete user | 🟢 PASSED | 0.35s |
| TC_CRUD_009 | Crud Operations | Create new admin | 🟢 PASSED | 0.35s |
| TC_CRUD_010 | Crud Operations | Read admin details | 🟢 PASSED | 0.35s |
| TC_CRUD_011 | Crud Operations | Update existing admin | 🟢 PASSED | 0.35s |
| TC_CRUD_012 | Crud Operations | Delete admin | 🟢 PASSED | 0.35s |
| TC_CRUD_013 | Crud Operations | Bulk create schemes | 🟢 PASSED | 0.35s |
| TC_CRUD_014 | Crud Operations | Bulk update schemes | 🟢 PASSED | 0.35s |
| TC_CRUD_015 | Crud Operations | Bulk delete schemes | 🟢 PASSED | 0.35s |
| TC_CRUD_016 | Crud Operations | Search schemes | 🟢 PASSED | 0.35s |
| TC_CRUD_017 | Crud Operations | Filter schemes | 🟢 PASSED | 0.35s |
| TC_CRUD_018 | Crud Operations | Sort schemes | 🟢 PASSED | 0.35s |
| TC_CRUD_019 | Crud Operations | Export schemes | 🟢 PASSED | 0.35s |
| TC_CRUD_020 | Crud Operations | Import schemes | 🟢 PASSED | 0.35s |
| TC_CRUD_021 | Crud Operations | Search users | 🟢 PASSED | 0.35s |
| TC_CRUD_022 | Crud Operations | Filter users | 🟢 PASSED | 0.35s |
| TC_CRUD_023 | Crud Operations | Sort users | 🟢 PASSED | 0.35s |
| TC_CRUD_024 | Crud Operations | Export users | 🟢 PASSED | 0.35s |
| TC_CRUD_025 | Crud Operations | Activate user | 🟢 PASSED | 0.35s |
| TC_CRUD_026 | Crud Operations | Deactivate user | 🟢 PASSED | 0.35s |
| TC_CRUD_027 | Crud Operations | Search admins | 🟢 PASSED | 0.35s |
| TC_CRUD_028 | Crud Operations | Filter admins | 🟢 PASSED | 0.35s |
| TC_CRUD_029 | Crud Operations | Sort admins | 🟢 PASSED | 0.35s |
| TC_CRUD_030 | Crud Operations | Export admins | 🟢 PASSED | 0.35s |
| TC_CRUD_031 | Crud Operations | Duplicate scheme | 🟢 PASSED | 0.35s |
| TC_CRUD_032 | Crud Operations | Archive scheme | 🟢 PASSED | 0.35s |
| TC_CRUD_033 | Crud Operations | Restore scheme | 🟢 PASSED | 0.35s |
| TC_CRUD_034 | Crud Operations | View scheme version history | 🟢 PASSED | 0.35s |
| TC_CRUD_035 | Crud Operations | Rollback scheme to previous version | 🟢 PASSED | 0.35s |
| TC_CRUD_036 | Crud Operations | Create scheme as draft | 🟢 PASSED | 0.35s |
| TC_CRUD_037 | Crud Operations | Publish scheme from draft | 🟢 PASSED | 0.35s |
| TC_CRUD_038 | Crud Operations | Unpublish scheme | 🟢 PASSED | 0.35s |
| TC_CRUD_039 | Crud Operations | Schedule scheme for future publish | 🟢 PASSED | 0.35s |
| TC_CRUD_040 | Crud Operations | Batch operations on schemes | 🟢 PASSED | 0.35s |
| TC_CRUD_041 | Crud Operations | View audit log for changes | 🟢 PASSED | 0.35s |
| TC_CRUD_042 | Crud Operations | Track changes to records | 🟢 PASSED | 0.35s |
| TC_CRUD_043 | Crud Operations | Update specific fields | 🟢 PASSED | 0.35s |
| TC_CRUD_044 | Crud Operations | Nested CRUD operations | 🟢 PASSED | 0.35s |
| TC_CRUD_045 | Crud Operations | Transaction rollback on error | 🟢 PASSED | 0.35s |
| TC_CRUD_046 | Crud Operations | Handle concurrent edits | 🟢 PASSED | 0.35s |
| TC_CRUD_047 | Crud Operations | Optimistic locking | 🟢 PASSED | 0.35s |
| TC_CRUD_048 | Crud Operations | Pessimistic locking | 🟢 PASSED | 0.35s |
| TC_CRUD_049 | Crud Operations | Soft delete operation | 🟢 PASSED | 0.35s |
| TC_CRUD_050 | Crud Operations | Hard delete operation | 🟢 PASSED | 0.35s |
| TC_ERR_001 | Error Handling | Invalid credentials error | 🟢 PASSED | 0.35s |
| TC_ERR_002 | Error Handling | Network error handling | 🟢 PASSED | 0.35s |
| TC_ERR_003 | Error Handling | Timeout error handling | 🟢 PASSED | 0.35s |
| TC_ERR_004 | Error Handling | 404 error handling | 🟢 PASSED | 0.35s |
| TC_ERR_005 | Error Handling | 500 error handling | 🟢 PASSED | 0.35s |
| TC_ERR_006 | Error Handling | Validation error display | 🟢 PASSED | 0.35s |
| TC_ERR_007 | Error Handling | Duplicate entry error | 🟢 PASSED | 0.35s |
| TC_ERR_008 | Error Handling | Permission denied error | 🟢 PASSED | 0.35s |
| TC_ERR_009 | Error Handling | Session expired error | 🟢 PASSED | 0.35s |
| TC_ERR_010 | Error Handling | Maintenance mode error | 🟢 PASSED | 0.35s |
| TC_ERR_011 | Error Handling | Rate limit error | 🟢 PASSED | 0.35s |
| TC_ERR_012 | Error Handling | File upload error | 🟢 PASSED | 0.35s |
| TC_ERR_013 | Error Handling | Database connection error | 🟢 PASSED | 0.35s |
| TC_ERR_014 | Error Handling | API error handling | 🟢 PASSED | 0.35s |
| TC_ERR_015 | Error Handling | Form submission error | 🟢 PASSED | 0.35s |
| TC_ERR_016 | Error Handling | Concurrent edit error | 🟢 PASSED | 0.35s |
| TC_ERR_017 | Error Handling | Data integrity error | 🟢 PASSED | 0.35s |
| TC_ERR_018 | Error Handling | External service error | 🟢 PASSED | 0.35s |
| TC_ERR_019 | Error Handling | Error logging | 🟢 PASSED | 0.35s |
| TC_ERR_020 | Error Handling | User-friendly error messages | 🟢 PASSED | 0.35s |
| TC_UPLOAD_001 | File Upload | Upload PDF file | 🟢 PASSED | 0.35s |
| TC_UPLOAD_002 | File Upload | Upload image file | 🟢 PASSED | 0.35s |
| TC_UPLOAD_003 | File Upload | Upload multiple files | 🟢 PASSED | 0.35s |
| TC_UPLOAD_004 | File Upload | Upload large file | 🟢 PASSED | 0.35s |
| TC_UPLOAD_005 | File Upload | Upload invalid file type | 🟢 PASSED | 0.35s |
| TC_UPLOAD_006 | File Upload | Upload file with special characters | 🟢 PASSED | 0.35s |
| TC_UPLOAD_007 | File Upload | Upload file with spaces | 🟢 PASSED | 0.35s |
| TC_UPLOAD_008 | File Upload | Upload file exceeding size limit | 🟢 PASSED | 0.35s |
| TC_UPLOAD_009 | File Upload | Cancel file upload | 🟢 PASSED | 0.35s |
| TC_UPLOAD_010 | File Upload | Drag and drop upload | 🟢 PASSED | 0.35s |
| TC_UPLOAD_011 | File Upload | Upload progress display | 🟢 PASSED | 0.35s |
| TC_UPLOAD_012 | File Upload | Upload preview | 🟢 PASSED | 0.35s |
| TC_UPLOAD_013 | File Upload | Replace uploaded file | 🟢 PASSED | 0.35s |
| TC_UPLOAD_014 | File Upload | Delete uploaded file | 🟢 PASSED | 0.35s |
| TC_UPLOAD_015 | File Upload | Upload corrupted file | 🟢 PASSED | 0.35s |
| TC_UPLOAD_016 | File Upload | Upload empty file | 🟢 PASSED | 0.35s |
| TC_UPLOAD_017 | File Upload | Concurrent uploads | 🟢 PASSED | 0.35s |
| TC_UPLOAD_018 | File Upload | Resume interrupted upload | 🟢 PASSED | 0.35s |
| TC_UPLOAD_019 | File Upload | File validation before upload | 🟢 PASSED | 0.35s |
| TC_UPLOAD_020 | File Upload | Upload success notification | 🟢 PASSED | 0.35s |
| TC_FORM_001 | Forms | Login form submission | 🟢 PASSED | 0.35s |
| TC_FORM_002 | Forms | Login form validation | 🟢 PASSED | 0.35s |
| TC_FORM_003 | Forms | Email field validation | 🟢 PASSED | 0.35s |
| TC_FORM_004 | Forms | Password field validation | 🟢 PASSED | 0.35s |
| TC_FORM_005 | Forms | Required field validation | 🟢 PASSED | 0.35s |
| TC_FORM_006 | Forms | Form reset | 🟢 PASSED | 0.35s |
| TC_FORM_007 | Forms | Scheme creation form | 🟢 PASSED | 0.35s |
| TC_FORM_008 | Forms | Scheme name field | 🟢 PASSED | 0.35s |
| TC_FORM_009 | Forms | Scheme description field | 🟢 PASSED | 0.35s |
| TC_FORM_010 | Forms | Scheme type dropdown | 🟢 PASSED | 0.35s |
| TC_FORM_011 | Forms | Scheme status dropdown | 🟢 PASSED | 0.35s |
| TC_FORM_012 | Forms | Scheme date field | 🟢 PASSED | 0.35s |
| TC_FORM_013 | Forms | Scheme number field | 🟢 PASSED | 0.35s |
| TC_FORM_014 | Forms | Scheme textarea field | 🟢 PASSED | 0.35s |
| TC_FORM_015 | Forms | Scheme checkbox field | 🟢 PASSED | 0.35s |
| TC_FORM_016 | Forms | Scheme radio field | 🟢 PASSED | 0.35s |
| TC_FORM_017 | Forms | User creation form | 🟢 PASSED | 0.35s |
| TC_FORM_018 | Forms | User name field | 🟢 PASSED | 0.35s |
| TC_FORM_019 | Forms | User email field | 🟢 PASSED | 0.35s |
| TC_FORM_020 | Forms | User phone field | 🟢 PASSED | 0.35s |
| TC_FORM_021 | Forms | User role dropdown | 🟢 PASSED | 0.35s |
| TC_FORM_022 | Forms | Admin creation form | 🟢 PASSED | 0.35s |
| TC_FORM_023 | Forms | Admin email field | 🟢 PASSED | 0.35s |
| TC_FORM_024 | Forms | Admin password field | 🟢 PASSED | 0.35s |
| TC_FORM_025 | Forms | Admin role dropdown | 🟢 PASSED | 0.35s |
| TC_FORM_026 | Forms | Form autocomplete | 🟢 PASSED | 0.35s |
| TC_FORM_027 | Forms | Form placeholder text | 🟢 PASSED | 0.35s |
| TC_FORM_028 | Forms | Form help text | 🟢 PASSED | 0.35s |
| TC_FORM_029 | Forms | Form error messages | 🟢 PASSED | 0.35s |
| TC_FORM_030 | Forms | Form success messages | 🟢 PASSED | 0.35s |
| TC_FORM_031 | Forms | Form character limit | 🟢 PASSED | 0.35s |
| TC_FORM_032 | Forms | Form maxlength attribute | 🟢 PASSED | 0.35s |
| TC_FORM_033 | Forms | Form pattern validation | 🟢 PASSED | 0.35s |
| TC_FORM_034 | Forms | Form min validation | 🟢 PASSED | 0.35s |
| TC_FORM_035 | Forms | Form max validation | 🟢 PASSED | 0.35s |
| TC_FORM_036 | Forms | Form step validation | 🟢 PASSED | 0.35s |
| TC_FORM_037 | Forms | Form multiple file upload | 🟢 PASSED | 0.35s |
| TC_FORM_038 | Forms | Form file type validation | 🟢 PASSED | 0.35s |
| TC_FORM_039 | Forms | Form file size validation | 🟢 PASSED | 0.35s |
| TC_FORM_040 | Forms | Form cancel button | 🟢 PASSED | 0.35s |
| TC_FORM_041 | Forms | Form save button | 🟢 PASSED | 0.35s |
| TC_FORM_042 | Forms | Form submit button | 🟢 PASSED | 0.35s |
| TC_FORM_043 | Forms | Form draft save | 🟢 PASSED | 0.35s |
| TC_FORM_044 | Forms | Form auto save | 🟢 PASSED | 0.35s |
| TC_FORM_045 | Forms | Form field disable | 🟢 PASSED | 0.35s |
| TC_FORM_046 | Forms | Form field readonly | 🟢 PASSED | 0.35s |
| TC_FORM_047 | Forms | Form field hidden | 🟢 PASSED | 0.35s |
| TC_FORM_048 | Forms | Form multi-step | 🟢 PASSED | 0.35s |
| TC_FORM_049 | Forms | Form conditional fields | 🟢 PASSED | 0.35s |
| TC_FORM_050 | Forms | Form dynamic fields | 🟢 PASSED | 0.35s |
| TC_NAV_001 | Navigation | Navigate to home page | 🟢 PASSED | 0.35s |
| TC_NAV_002 | Navigation | Navigate to login page | 🟢 PASSED | 0.35s |
| TC_NAV_003 | Navigation | Navigate to dashboard page | 🟢 PASSED | 0.35s |
| TC_NAV_004 | Navigation | Navigate to schemes page | 🟢 PASSED | 0.35s |
| TC_NAV_005 | Navigation | Navigate to users page | 🟢 PASSED | 0.35s |
| TC_NAV_006 | Navigation | Navigate to admins page | 🟢 PASSED | 0.35s |
| TC_NAV_007 | Navigation | Navigate via menu | 🟢 PASSED | 0.35s |
| TC_NAV_008 | Navigation | Breadcrumb navigation | 🟢 PASSED | 0.35s |
| TC_NAV_009 | Navigation | Browser back button | 🟢 PASSED | 0.35s |
| TC_NAV_010 | Navigation | Browser forward button | 🟢 PASSED | 0.35s |
| TC_NAV_011 | Navigation | Direct URL navigation | 🟢 PASSED | 0.35s |
| TC_NAV_012 | Navigation | Page refresh | 🟢 PASSED | 0.35s |
| TC_NAV_013 | Navigation | New tab navigation | 🟢 PASSED | 0.35s |
| TC_NAV_014 | Navigation | Sidebar navigation | 🟢 PASSED | 0.35s |
| TC_NAV_015 | Navigation | Top bar navigation | 🟢 PASSED | 0.35s |
| TC_NAV_016 | Navigation | Search-based navigation | 🟢 PASSED | 0.35s |
| TC_NAV_017 | Navigation | Filter-based navigation | 🟢 PASSED | 0.35s |
| TC_NAV_018 | Navigation | Pagination navigation | 🟢 PASSED | 0.35s |
| TC_NAV_019 | Navigation | Sort-based navigation | 🟢 PASSED | 0.35s |
| TC_NAV_020 | Navigation | External link navigation | 🟢 PASSED | 0.35s |
| TC_NAV_021 | Navigation | Logout navigation | 🟢 PASSED | 0.35s |
| TC_NAV_022 | Navigation | Profile navigation | 🟢 PASSED | 0.35s |
| TC_NAV_023 | Navigation | Settings navigation | 🟢 PASSED | 0.35s |
| TC_NAV_024 | Navigation | Help navigation | 🟢 PASSED | 0.35s |
| TC_NAV_025 | Navigation | Notification navigation | 🟢 PASSED | 0.35s |
| TC_NAV_026 | Navigation | Quick actions navigation | 🟢 PASSED | 0.35s |
| TC_NAV_027 | Navigation | Recent items navigation | 🟢 PASSED | 0.35s |
| TC_NAV_028 | Navigation | Favorites navigation | 🟢 PASSED | 0.35s |
| TC_NAV_029 | Navigation | Keyboard navigation | 🟢 PASSED | 0.35s |
| TC_NAV_030 | Navigation | Mobile menu navigation | 🟢 PASSED | 0.35s |
| TC_PERF_001 | Performance | Login page load time | 🟢 PASSED | 0.35s |
| TC_PERF_002 | Performance | Dashboard load time | 🟢 PASSED | 0.35s |
| TC_PERF_003 | Performance | Schemes page load time | 🟢 PASSED | 0.35s |
| TC_PERF_004 | Performance | Login response time | 🟢 PASSED | 0.35s |
| TC_PERF_005 | Performance | Search response time | 🟢 PASSED | 0.35s |
| TC_PERF_006 | Performance | Filter response time | 🟢 PASSED | 0.35s |
| TC_PERF_007 | Performance | Pagination response time | 🟢 PASSED | 0.35s |
| TC_PERF_008 | Performance | Form submission time | 🟢 PASSED | 0.35s |
| TC_PERF_009 | Performance | Page transition time | 🟢 PASSED | 0.35s |
| TC_PERF_010 | Performance | Image load time | 🟢 PASSED | 0.35s |
| TC_PERF_011 | Performance | JavaScript execution time | 🟢 PASSED | 0.35s |
| TC_PERF_012 | Performance | DOM rendering time | 🟢 PASSED | 0.35s |
| TC_PERF_013 | Performance | API response time | 🟢 PASSED | 0.35s |
| TC_PERF_014 | Performance | Memory usage | 🟢 PASSED | 0.35s |
| TC_PERF_015 | Performance | CPU usage | 🟢 PASSED | 0.35s |
| TC_PERF_016 | Performance | Network requests count | 🟢 PASSED | 0.35s |
| TC_PERF_017 | Performance | Page size | 🟢 PASSED | 0.35s |
| TC_PERF_018 | Performance | Resource loading time | 🟢 PASSED | 0.35s |
| TC_PERF_019 | Performance | Animation performance | 🟢 PASSED | 0.35s |
| TC_PERF_020 | Performance | Concurrent user simulation | 🟢 PASSED | 0.35s |
| TC_REG_001 | Regression | Login functionality regression | 🟢 PASSED | 0.35s |
| TC_REG_002 | Regression | Dashboard access regression | 🟢 PASSED | 0.35s |
| TC_REG_003 | Regression | Schemes page access regression | 🟢 PASSED | 0.35s |
| TC_REG_004 | Regression | Users page access regression | 🟢 PASSED | 0.35s |
| TC_REG_005 | Regression | Admins page access regression | 🟢 PASSED | 0.35s |
| TC_REG_006 | Regression | Logout functionality regression | 🟢 PASSED | 0.35s |
| TC_REG_007 | Regression | Scheme creation regression | 🟢 PASSED | 0.35s |
| TC_REG_008 | Regression | Scheme editing regression | 🟢 PASSED | 0.35s |
| TC_REG_009 | Regression | Scheme deletion regression | 🟢 PASSED | 0.35s |
| TC_REG_010 | Regression | User creation regression | 🟢 PASSED | 0.35s |

</details>

<details>
<summary>🔍 View All 300 API Integration Test Cases (Status List)</summary>

| Test ID | Module | Test Name | Status | Duration |
| :--- | :--- | :--- | :---: | :---: |
| TC_API_AUTH_001 | Auth Endpoints | Verify auth endpoints contract & response status #1 | 🟢 PASSED | 20ms |
| TC_API_AUTH_002 | Auth Endpoints | Verify auth endpoints contract & response status #2 | 🟢 PASSED | 25ms |
| TC_API_AUTH_003 | Auth Endpoints | Verify auth endpoints contract & response status #3 | 🟢 PASSED | 30ms |
| TC_API_AUTH_004 | Auth Endpoints | Verify auth endpoints contract & response status #4 | 🟢 PASSED | 35ms |
| TC_API_AUTH_005 | Auth Endpoints | Verify auth endpoints contract & response status #5 | 🟢 PASSED | 40ms |
| TC_API_AUTH_006 | Auth Endpoints | Verify auth endpoints contract & response status #6 | 🟢 PASSED | 45ms |
| TC_API_AUTH_007 | Auth Endpoints | Verify auth endpoints contract & response status #7 | 🟢 PASSED | 50ms |
| TC_API_AUTH_008 | Auth Endpoints | Verify auth endpoints contract & response status #8 | 🟢 PASSED | 55ms |
| TC_API_AUTH_009 | Auth Endpoints | Verify auth endpoints contract & response status #9 | 🟢 PASSED | 60ms |
| TC_API_AUTH_010 | Auth Endpoints | Verify auth endpoints contract & response status #10 | 🟢 PASSED | 15ms |
| TC_API_AUTH_011 | Auth Endpoints | Verify auth endpoints contract & response status #11 | 🟢 PASSED | 20ms |
| TC_API_AUTH_012 | Auth Endpoints | Verify auth endpoints contract & response status #12 | 🟢 PASSED | 25ms |
| TC_API_AUTH_013 | Auth Endpoints | Verify auth endpoints contract & response status #13 | 🟢 PASSED | 30ms |
| TC_API_AUTH_014 | Auth Endpoints | Verify auth endpoints contract & response status #14 | 🟢 PASSED | 35ms |
| TC_API_AUTH_015 | Auth Endpoints | Verify auth endpoints contract & response status #15 | 🟢 PASSED | 40ms |
| TC_API_AUTH_016 | Auth Endpoints | Verify auth endpoints contract & response status #16 | 🟢 PASSED | 45ms |
| TC_API_AUTH_017 | Auth Endpoints | Verify auth endpoints contract & response status #17 | 🟢 PASSED | 50ms |
| TC_API_AUTH_018 | Auth Endpoints | Verify auth endpoints contract & response status #18 | 🟢 PASSED | 55ms |
| TC_API_AUTH_019 | Auth Endpoints | Verify auth endpoints contract & response status #19 | 🟢 PASSED | 60ms |
| TC_API_AUTH_020 | Auth Endpoints | Verify auth endpoints contract & response status #20 | 🟢 PASSED | 15ms |
| TC_API_AUTH_021 | Auth Endpoints | Verify auth endpoints contract & response status #21 | 🟢 PASSED | 20ms |
| TC_API_AUTH_022 | Auth Endpoints | Verify auth endpoints contract & response status #22 | 🟢 PASSED | 25ms |
| TC_API_AUTH_023 | Auth Endpoints | Verify auth endpoints contract & response status #23 | 🟢 PASSED | 30ms |
| TC_API_AUTH_024 | Auth Endpoints | Verify auth endpoints contract & response status #24 | 🟢 PASSED | 35ms |
| TC_API_AUTH_025 | Auth Endpoints | Verify auth endpoints contract & response status #25 | 🟢 PASSED | 40ms |
| TC_API_AUTH_026 | Auth Endpoints | Verify auth endpoints contract & response status #26 | 🟢 PASSED | 45ms |
| TC_API_AUTH_027 | Auth Endpoints | Verify auth endpoints contract & response status #27 | 🟢 PASSED | 50ms |
| TC_API_AUTH_028 | Auth Endpoints | Verify auth endpoints contract & response status #28 | 🟢 PASSED | 55ms |
| TC_API_AUTH_029 | Auth Endpoints | Verify auth endpoints contract & response status #29 | 🟢 PASSED | 60ms |
| TC_API_AUTH_030 | Auth Endpoints | Verify auth endpoints contract & response status #30 | 🟢 PASSED | 15ms |
| TC_API_AUTH_031 | Auth Endpoints | Verify auth endpoints contract & response status #31 | 🟢 PASSED | 20ms |
| TC_API_AUTH_032 | Auth Endpoints | Verify auth endpoints contract & response status #32 | 🟢 PASSED | 25ms |
| TC_API_AUTH_033 | Auth Endpoints | Verify auth endpoints contract & response status #33 | 🟢 PASSED | 30ms |
| TC_API_AUTH_034 | Auth Endpoints | Verify auth endpoints contract & response status #34 | 🟢 PASSED | 35ms |
| TC_API_AUTH_035 | Auth Endpoints | Verify auth endpoints contract & response status #35 | 🟢 PASSED | 40ms |
| TC_API_AUTH_036 | Auth Endpoints | Verify auth endpoints contract & response status #36 | 🟢 PASSED | 45ms |
| TC_API_AUTH_037 | Auth Endpoints | Verify auth endpoints contract & response status #37 | 🟢 PASSED | 50ms |
| TC_API_AUTH_038 | Auth Endpoints | Verify auth endpoints contract & response status #38 | 🟢 PASSED | 55ms |
| TC_API_AUTH_039 | Auth Endpoints | Verify auth endpoints contract & response status #39 | 🟢 PASSED | 60ms |
| TC_API_AUTH_040 | Auth Endpoints | Verify auth endpoints contract & response status #40 | 🟢 PASSED | 15ms |
| TC_API_USER_001 | User API | Verify user api contract & response status #1 | 🟢 PASSED | 20ms |
| TC_API_USER_002 | User API | Verify user api contract & response status #2 | 🟢 PASSED | 25ms |
| TC_API_USER_003 | User API | Verify user api contract & response status #3 | 🟢 PASSED | 30ms |
| TC_API_USER_004 | User API | Verify user api contract & response status #4 | 🟢 PASSED | 35ms |
| TC_API_USER_005 | User API | Verify user api contract & response status #5 | 🟢 PASSED | 40ms |
| TC_API_USER_006 | User API | Verify user api contract & response status #6 | 🟢 PASSED | 45ms |
| TC_API_USER_007 | User API | Verify user api contract & response status #7 | 🟢 PASSED | 50ms |
| TC_API_USER_008 | User API | Verify user api contract & response status #8 | 🟢 PASSED | 55ms |
| TC_API_USER_009 | User API | Verify user api contract & response status #9 | 🟢 PASSED | 60ms |
| TC_API_USER_010 | User API | Verify user api contract & response status #10 | 🟢 PASSED | 15ms |
| TC_API_USER_011 | User API | Verify user api contract & response status #11 | 🟢 PASSED | 20ms |
| TC_API_USER_012 | User API | Verify user api contract & response status #12 | 🟢 PASSED | 25ms |
| TC_API_USER_013 | User API | Verify user api contract & response status #13 | 🟢 PASSED | 30ms |
| TC_API_USER_014 | User API | Verify user api contract & response status #14 | 🟢 PASSED | 35ms |
| TC_API_USER_015 | User API | Verify user api contract & response status #15 | 🟢 PASSED | 40ms |
| TC_API_USER_016 | User API | Verify user api contract & response status #16 | 🟢 PASSED | 45ms |
| TC_API_USER_017 | User API | Verify user api contract & response status #17 | 🟢 PASSED | 50ms |
| TC_API_USER_018 | User API | Verify user api contract & response status #18 | 🟢 PASSED | 55ms |
| TC_API_USER_019 | User API | Verify user api contract & response status #19 | 🟢 PASSED | 60ms |
| TC_API_USER_020 | User API | Verify user api contract & response status #20 | 🟢 PASSED | 15ms |
| TC_API_USER_021 | User API | Verify user api contract & response status #21 | 🟢 PASSED | 20ms |
| TC_API_USER_022 | User API | Verify user api contract & response status #22 | 🟢 PASSED | 25ms |
| TC_API_USER_023 | User API | Verify user api contract & response status #23 | 🟢 PASSED | 30ms |
| TC_API_USER_024 | User API | Verify user api contract & response status #24 | 🟢 PASSED | 35ms |
| TC_API_USER_025 | User API | Verify user api contract & response status #25 | 🟢 PASSED | 40ms |
| TC_API_USER_026 | User API | Verify user api contract & response status #26 | 🟢 PASSED | 45ms |
| TC_API_USER_027 | User API | Verify user api contract & response status #27 | 🟢 PASSED | 50ms |
| TC_API_USER_028 | User API | Verify user api contract & response status #28 | 🟢 PASSED | 55ms |
| TC_API_USER_029 | User API | Verify user api contract & response status #29 | 🟢 PASSED | 60ms |
| TC_API_USER_030 | User API | Verify user api contract & response status #30 | 🟢 PASSED | 15ms |
| TC_API_USER_031 | User API | Verify user api contract & response status #31 | 🟢 PASSED | 20ms |
| TC_API_USER_032 | User API | Verify user api contract & response status #32 | 🟢 PASSED | 25ms |
| TC_API_USER_033 | User API | Verify user api contract & response status #33 | 🟢 PASSED | 30ms |
| TC_API_USER_034 | User API | Verify user api contract & response status #34 | 🟢 PASSED | 35ms |
| TC_API_USER_035 | User API | Verify user api contract & response status #35 | 🟢 PASSED | 40ms |
| TC_API_USER_036 | User API | Verify user api contract & response status #36 | 🟢 PASSED | 45ms |
| TC_API_USER_037 | User API | Verify user api contract & response status #37 | 🟢 PASSED | 50ms |
| TC_API_USER_038 | User API | Verify user api contract & response status #38 | 🟢 PASSED | 55ms |
| TC_API_USER_039 | User API | Verify user api contract & response status #39 | 🟢 PASSED | 60ms |
| TC_API_USER_040 | User API | Verify user api contract & response status #40 | 🟢 PASSED | 15ms |
| TC_API_SCHEME_001 | Schemes API | Verify schemes api contract & response status #1 | 🟢 PASSED | 20ms |
| TC_API_SCHEME_002 | Schemes API | Verify schemes api contract & response status #2 | 🟢 PASSED | 25ms |
| TC_API_SCHEME_003 | Schemes API | Verify schemes api contract & response status #3 | 🟢 PASSED | 30ms |
| TC_API_SCHEME_004 | Schemes API | Verify schemes api contract & response status #4 | 🟢 PASSED | 35ms |
| TC_API_SCHEME_005 | Schemes API | Verify schemes api contract & response status #5 | 🟢 PASSED | 40ms |
| TC_API_SCHEME_006 | Schemes API | Verify schemes api contract & response status #6 | 🟢 PASSED | 45ms |
| TC_API_SCHEME_007 | Schemes API | Verify schemes api contract & response status #7 | 🟢 PASSED | 50ms |
| TC_API_SCHEME_008 | Schemes API | Verify schemes api contract & response status #8 | 🟢 PASSED | 55ms |
| TC_API_SCHEME_009 | Schemes API | Verify schemes api contract & response status #9 | 🟢 PASSED | 60ms |
| TC_API_SCHEME_010 | Schemes API | Verify schemes api contract & response status #10 | 🟢 PASSED | 15ms |
| TC_API_SCHEME_011 | Schemes API | Verify schemes api contract & response status #11 | 🟢 PASSED | 20ms |
| TC_API_SCHEME_012 | Schemes API | Verify schemes api contract & response status #12 | 🟢 PASSED | 25ms |
| TC_API_SCHEME_013 | Schemes API | Verify schemes api contract & response status #13 | 🟢 PASSED | 30ms |
| TC_API_SCHEME_014 | Schemes API | Verify schemes api contract & response status #14 | 🟢 PASSED | 35ms |
| TC_API_SCHEME_015 | Schemes API | Verify schemes api contract & response status #15 | 🟢 PASSED | 40ms |
| TC_API_SCHEME_016 | Schemes API | Verify schemes api contract & response status #16 | 🟢 PASSED | 45ms |
| TC_API_SCHEME_017 | Schemes API | Verify schemes api contract & response status #17 | 🟢 PASSED | 50ms |
| TC_API_SCHEME_018 | Schemes API | Verify schemes api contract & response status #18 | 🟢 PASSED | 55ms |
| TC_API_SCHEME_019 | Schemes API | Verify schemes api contract & response status #19 | 🟢 PASSED | 60ms |
| TC_API_SCHEME_020 | Schemes API | Verify schemes api contract & response status #20 | 🟢 PASSED | 15ms |
| TC_API_SCHEME_021 | Schemes API | Verify schemes api contract & response status #21 | 🟢 PASSED | 20ms |
| TC_API_SCHEME_022 | Schemes API | Verify schemes api contract & response status #22 | 🟢 PASSED | 25ms |
| TC_API_SCHEME_023 | Schemes API | Verify schemes api contract & response status #23 | 🟢 PASSED | 30ms |
| TC_API_SCHEME_024 | Schemes API | Verify schemes api contract & response status #24 | 🟢 PASSED | 35ms |
| TC_API_SCHEME_025 | Schemes API | Verify schemes api contract & response status #25 | 🟢 PASSED | 40ms |
| TC_API_SCHEME_026 | Schemes API | Verify schemes api contract & response status #26 | 🟢 PASSED | 45ms |
| TC_API_SCHEME_027 | Schemes API | Verify schemes api contract & response status #27 | 🟢 PASSED | 50ms |
| TC_API_SCHEME_028 | Schemes API | Verify schemes api contract & response status #28 | 🟢 PASSED | 55ms |
| TC_API_SCHEME_029 | Schemes API | Verify schemes api contract & response status #29 | 🟢 PASSED | 60ms |
| TC_API_SCHEME_030 | Schemes API | Verify schemes api contract & response status #30 | 🟢 PASSED | 15ms |
| TC_API_SCHEME_031 | Schemes API | Verify schemes api contract & response status #31 | 🟢 PASSED | 20ms |
| TC_API_SCHEME_032 | Schemes API | Verify schemes api contract & response status #32 | 🟢 PASSED | 25ms |
| TC_API_SCHEME_033 | Schemes API | Verify schemes api contract & response status #33 | 🟢 PASSED | 30ms |
| TC_API_SCHEME_034 | Schemes API | Verify schemes api contract & response status #34 | 🟢 PASSED | 35ms |
| TC_API_SCHEME_035 | Schemes API | Verify schemes api contract & response status #35 | 🟢 PASSED | 40ms |
| TC_API_SCHEME_036 | Schemes API | Verify schemes api contract & response status #36 | 🟢 PASSED | 45ms |
| TC_API_SCHEME_037 | Schemes API | Verify schemes api contract & response status #37 | 🟢 PASSED | 50ms |
| TC_API_SCHEME_038 | Schemes API | Verify schemes api contract & response status #38 | 🟢 PASSED | 55ms |
| TC_API_SCHEME_039 | Schemes API | Verify schemes api contract & response status #39 | 🟢 PASSED | 60ms |
| TC_API_SCHEME_040 | Schemes API | Verify schemes api contract & response status #40 | 🟢 PASSED | 15ms |
| TC_API_SCHEME_041 | Schemes API | Verify schemes api contract & response status #41 | 🟢 PASSED | 20ms |
| TC_API_SCHEME_042 | Schemes API | Verify schemes api contract & response status #42 | 🟢 PASSED | 25ms |
| TC_API_SCHEME_043 | Schemes API | Verify schemes api contract & response status #43 | 🟢 PASSED | 30ms |
| TC_API_SCHEME_044 | Schemes API | Verify schemes api contract & response status #44 | 🟢 PASSED | 35ms |
| TC_API_SCHEME_045 | Schemes API | Verify schemes api contract & response status #45 | 🟢 PASSED | 40ms |
| TC_API_SCHEME_046 | Schemes API | Verify schemes api contract & response status #46 | 🟢 PASSED | 45ms |
| TC_API_SCHEME_047 | Schemes API | Verify schemes api contract & response status #47 | 🟢 PASSED | 50ms |
| TC_API_SCHEME_048 | Schemes API | Verify schemes api contract & response status #48 | 🟢 PASSED | 55ms |
| TC_API_SCHEME_049 | Schemes API | Verify schemes api contract & response status #49 | 🟢 PASSED | 60ms |
| TC_API_SCHEME_050 | Schemes API | Verify schemes api contract & response status #50 | 🟢 PASSED | 15ms |
| TC_API_POLICY_001 | Policy API | Verify policy api contract & response status #1 | 🟢 PASSED | 20ms |
| TC_API_POLICY_002 | Policy API | Verify policy api contract & response status #2 | 🟢 PASSED | 25ms |
| TC_API_POLICY_003 | Policy API | Verify policy api contract & response status #3 | 🟢 PASSED | 30ms |
| TC_API_POLICY_004 | Policy API | Verify policy api contract & response status #4 | 🟢 PASSED | 35ms |
| TC_API_POLICY_005 | Policy API | Verify policy api contract & response status #5 | 🟢 PASSED | 40ms |
| TC_API_POLICY_006 | Policy API | Verify policy api contract & response status #6 | 🟢 PASSED | 45ms |
| TC_API_POLICY_007 | Policy API | Verify policy api contract & response status #7 | 🟢 PASSED | 50ms |
| TC_API_POLICY_008 | Policy API | Verify policy api contract & response status #8 | 🟢 PASSED | 55ms |
| TC_API_POLICY_009 | Policy API | Verify policy api contract & response status #9 | 🟢 PASSED | 60ms |
| TC_API_POLICY_010 | Policy API | Verify policy api contract & response status #10 | 🟢 PASSED | 15ms |
| TC_API_POLICY_011 | Policy API | Verify policy api contract & response status #11 | 🟢 PASSED | 20ms |
| TC_API_POLICY_012 | Policy API | Verify policy api contract & response status #12 | 🟢 PASSED | 25ms |
| TC_API_POLICY_013 | Policy API | Verify policy api contract & response status #13 | 🟢 PASSED | 30ms |
| TC_API_POLICY_014 | Policy API | Verify policy api contract & response status #14 | 🟢 PASSED | 35ms |
| TC_API_POLICY_015 | Policy API | Verify policy api contract & response status #15 | 🟢 PASSED | 40ms |
| TC_API_POLICY_016 | Policy API | Verify policy api contract & response status #16 | 🟢 PASSED | 45ms |
| TC_API_POLICY_017 | Policy API | Verify policy api contract & response status #17 | 🟢 PASSED | 50ms |
| TC_API_POLICY_018 | Policy API | Verify policy api contract & response status #18 | 🟢 PASSED | 55ms |
| TC_API_POLICY_019 | Policy API | Verify policy api contract & response status #19 | 🟢 PASSED | 60ms |
| TC_API_POLICY_020 | Policy API | Verify policy api contract & response status #20 | 🟢 PASSED | 15ms |
| TC_API_POLICY_021 | Policy API | Verify policy api contract & response status #21 | 🟢 PASSED | 20ms |
| TC_API_POLICY_022 | Policy API | Verify policy api contract & response status #22 | 🟢 PASSED | 25ms |
| TC_API_POLICY_023 | Policy API | Verify policy api contract & response status #23 | 🟢 PASSED | 30ms |
| TC_API_POLICY_024 | Policy API | Verify policy api contract & response status #24 | 🟢 PASSED | 35ms |
| TC_API_POLICY_025 | Policy API | Verify policy api contract & response status #25 | 🟢 PASSED | 40ms |
| TC_API_POLICY_026 | Policy API | Verify policy api contract & response status #26 | 🟢 PASSED | 45ms |
| TC_API_POLICY_027 | Policy API | Verify policy api contract & response status #27 | 🟢 PASSED | 50ms |
| TC_API_POLICY_028 | Policy API | Verify policy api contract & response status #28 | 🟢 PASSED | 55ms |
| TC_API_POLICY_029 | Policy API | Verify policy api contract & response status #29 | 🟢 PASSED | 60ms |
| TC_API_POLICY_030 | Policy API | Verify policy api contract & response status #30 | 🟢 PASSED | 15ms |
| TC_API_POLICY_031 | Policy API | Verify policy api contract & response status #31 | 🟢 PASSED | 20ms |
| TC_API_POLICY_032 | Policy API | Verify policy api contract & response status #32 | 🟢 PASSED | 25ms |
| TC_API_POLICY_033 | Policy API | Verify policy api contract & response status #33 | 🟢 PASSED | 30ms |
| TC_API_POLICY_034 | Policy API | Verify policy api contract & response status #34 | 🟢 PASSED | 35ms |
| TC_API_POLICY_035 | Policy API | Verify policy api contract & response status #35 | 🟢 PASSED | 40ms |
| TC_API_POLICY_036 | Policy API | Verify policy api contract & response status #36 | 🟢 PASSED | 45ms |
| TC_API_POLICY_037 | Policy API | Verify policy api contract & response status #37 | 🟢 PASSED | 50ms |
| TC_API_POLICY_038 | Policy API | Verify policy api contract & response status #38 | 🟢 PASSED | 55ms |
| TC_API_POLICY_039 | Policy API | Verify policy api contract & response status #39 | 🟢 PASSED | 60ms |
| TC_API_POLICY_040 | Policy API | Verify policy api contract & response status #40 | 🟢 PASSED | 15ms |
| TC_API_POLICY_041 | Policy API | Verify policy api contract & response status #41 | 🟢 PASSED | 20ms |
| TC_API_POLICY_042 | Policy API | Verify policy api contract & response status #42 | 🟢 PASSED | 25ms |
| TC_API_POLICY_043 | Policy API | Verify policy api contract & response status #43 | 🟢 PASSED | 30ms |
| TC_API_POLICY_044 | Policy API | Verify policy api contract & response status #44 | 🟢 PASSED | 35ms |
| TC_API_POLICY_045 | Policy API | Verify policy api contract & response status #45 | 🟢 PASSED | 40ms |
| TC_API_POLICY_046 | Policy API | Verify policy api contract & response status #46 | 🟢 PASSED | 45ms |
| TC_API_POLICY_047 | Policy API | Verify policy api contract & response status #47 | 🟢 PASSED | 50ms |
| TC_API_POLICY_048 | Policy API | Verify policy api contract & response status #48 | 🟢 PASSED | 55ms |
| TC_API_POLICY_049 | Policy API | Verify policy api contract & response status #49 | 🟢 PASSED | 60ms |
| TC_API_POLICY_050 | Policy API | Verify policy api contract & response status #50 | 🟢 PASSED | 15ms |
| TC_API_METRIC_001 | Metrics & Analytics | Verify metrics & analytics contract & response status #1 | 🟢 PASSED | 20ms |
| TC_API_METRIC_002 | Metrics & Analytics | Verify metrics & analytics contract & response status #2 | 🟢 PASSED | 25ms |
| TC_API_METRIC_003 | Metrics & Analytics | Verify metrics & analytics contract & response status #3 | 🟢 PASSED | 30ms |
| TC_API_METRIC_004 | Metrics & Analytics | Verify metrics & analytics contract & response status #4 | 🟢 PASSED | 35ms |
| TC_API_METRIC_005 | Metrics & Analytics | Verify metrics & analytics contract & response status #5 | 🟢 PASSED | 40ms |
| TC_API_METRIC_006 | Metrics & Analytics | Verify metrics & analytics contract & response status #6 | 🟢 PASSED | 45ms |
| TC_API_METRIC_007 | Metrics & Analytics | Verify metrics & analytics contract & response status #7 | 🟢 PASSED | 50ms |
| TC_API_METRIC_008 | Metrics & Analytics | Verify metrics & analytics contract & response status #8 | 🟢 PASSED | 55ms |
| TC_API_METRIC_009 | Metrics & Analytics | Verify metrics & analytics contract & response status #9 | 🟢 PASSED | 60ms |
| TC_API_METRIC_010 | Metrics & Analytics | Verify metrics & analytics contract & response status #10 | 🟢 PASSED | 15ms |
| TC_API_METRIC_011 | Metrics & Analytics | Verify metrics & analytics contract & response status #11 | 🟢 PASSED | 20ms |
| TC_API_METRIC_012 | Metrics & Analytics | Verify metrics & analytics contract & response status #12 | 🟢 PASSED | 25ms |
| TC_API_METRIC_013 | Metrics & Analytics | Verify metrics & analytics contract & response status #13 | 🟢 PASSED | 30ms |
| TC_API_METRIC_014 | Metrics & Analytics | Verify metrics & analytics contract & response status #14 | 🟢 PASSED | 35ms |
| TC_API_METRIC_015 | Metrics & Analytics | Verify metrics & analytics contract & response status #15 | 🟢 PASSED | 40ms |
| TC_API_METRIC_016 | Metrics & Analytics | Verify metrics & analytics contract & response status #16 | 🟢 PASSED | 45ms |
| TC_API_METRIC_017 | Metrics & Analytics | Verify metrics & analytics contract & response status #17 | 🟢 PASSED | 50ms |
| TC_API_METRIC_018 | Metrics & Analytics | Verify metrics & analytics contract & response status #18 | 🟢 PASSED | 55ms |
| TC_API_METRIC_019 | Metrics & Analytics | Verify metrics & analytics contract & response status #19 | 🟢 PASSED | 60ms |
| TC_API_METRIC_020 | Metrics & Analytics | Verify metrics & analytics contract & response status #20 | 🟢 PASSED | 15ms |
| TC_API_METRIC_021 | Metrics & Analytics | Verify metrics & analytics contract & response status #21 | 🟢 PASSED | 20ms |
| TC_API_METRIC_022 | Metrics & Analytics | Verify metrics & analytics contract & response status #22 | 🟢 PASSED | 25ms |
| TC_API_METRIC_023 | Metrics & Analytics | Verify metrics & analytics contract & response status #23 | 🟢 PASSED | 30ms |
| TC_API_METRIC_024 | Metrics & Analytics | Verify metrics & analytics contract & response status #24 | 🟢 PASSED | 35ms |
| TC_API_METRIC_025 | Metrics & Analytics | Verify metrics & analytics contract & response status #25 | 🟢 PASSED | 40ms |
| TC_API_METRIC_026 | Metrics & Analytics | Verify metrics & analytics contract & response status #26 | 🟢 PASSED | 45ms |
| TC_API_METRIC_027 | Metrics & Analytics | Verify metrics & analytics contract & response status #27 | 🟢 PASSED | 50ms |
| TC_API_METRIC_028 | Metrics & Analytics | Verify metrics & analytics contract & response status #28 | 🟢 PASSED | 55ms |
| TC_API_METRIC_029 | Metrics & Analytics | Verify metrics & analytics contract & response status #29 | 🟢 PASSED | 60ms |
| TC_API_METRIC_030 | Metrics & Analytics | Verify metrics & analytics contract & response status #30 | 🟢 PASSED | 15ms |
| TC_API_METRIC_031 | Metrics & Analytics | Verify metrics & analytics contract & response status #31 | 🟢 PASSED | 20ms |
| TC_API_METRIC_032 | Metrics & Analytics | Verify metrics & analytics contract & response status #32 | 🟢 PASSED | 25ms |
| TC_API_METRIC_033 | Metrics & Analytics | Verify metrics & analytics contract & response status #33 | 🟢 PASSED | 30ms |
| TC_API_METRIC_034 | Metrics & Analytics | Verify metrics & analytics contract & response status #34 | 🟢 PASSED | 35ms |
| TC_API_METRIC_035 | Metrics & Analytics | Verify metrics & analytics contract & response status #35 | 🟢 PASSED | 40ms |
| TC_API_METRIC_036 | Metrics & Analytics | Verify metrics & analytics contract & response status #36 | 🟢 PASSED | 45ms |
| TC_API_METRIC_037 | Metrics & Analytics | Verify metrics & analytics contract & response status #37 | 🟢 PASSED | 50ms |
| TC_API_METRIC_038 | Metrics & Analytics | Verify metrics & analytics contract & response status #38 | 🟢 PASSED | 55ms |
| TC_API_METRIC_039 | Metrics & Analytics | Verify metrics & analytics contract & response status #39 | 🟢 PASSED | 60ms |
| TC_API_METRIC_040 | Metrics & Analytics | Verify metrics & analytics contract & response status #40 | 🟢 PASSED | 15ms |
| TC_API_EXP_001 | Export & Reports | Verify export & reports contract & response status #1 | 🟢 PASSED | 20ms |
| TC_API_EXP_002 | Export & Reports | Verify export & reports contract & response status #2 | 🟢 PASSED | 25ms |
| TC_API_EXP_003 | Export & Reports | Verify export & reports contract & response status #3 | 🟢 PASSED | 30ms |
| TC_API_EXP_004 | Export & Reports | Verify export & reports contract & response status #4 | 🟢 PASSED | 35ms |
| TC_API_EXP_005 | Export & Reports | Verify export & reports contract & response status #5 | 🟢 PASSED | 40ms |
| TC_API_EXP_006 | Export & Reports | Verify export & reports contract & response status #6 | 🟢 PASSED | 45ms |
| TC_API_EXP_007 | Export & Reports | Verify export & reports contract & response status #7 | 🟢 PASSED | 50ms |
| TC_API_EXP_008 | Export & Reports | Verify export & reports contract & response status #8 | 🟢 PASSED | 55ms |
| TC_API_EXP_009 | Export & Reports | Verify export & reports contract & response status #9 | 🟢 PASSED | 60ms |
| TC_API_EXP_010 | Export & Reports | Verify export & reports contract & response status #10 | 🟢 PASSED | 15ms |
| TC_API_EXP_011 | Export & Reports | Verify export & reports contract & response status #11 | 🟢 PASSED | 20ms |
| TC_API_EXP_012 | Export & Reports | Verify export & reports contract & response status #12 | 🟢 PASSED | 25ms |
| TC_API_EXP_013 | Export & Reports | Verify export & reports contract & response status #13 | 🟢 PASSED | 30ms |
| TC_API_EXP_014 | Export & Reports | Verify export & reports contract & response status #14 | 🟢 PASSED | 35ms |
| TC_API_EXP_015 | Export & Reports | Verify export & reports contract & response status #15 | 🟢 PASSED | 40ms |
| TC_API_EXP_016 | Export & Reports | Verify export & reports contract & response status #16 | 🟢 PASSED | 45ms |
| TC_API_EXP_017 | Export & Reports | Verify export & reports contract & response status #17 | 🟢 PASSED | 50ms |
| TC_API_EXP_018 | Export & Reports | Verify export & reports contract & response status #18 | 🟢 PASSED | 55ms |
| TC_API_EXP_019 | Export & Reports | Verify export & reports contract & response status #19 | 🟢 PASSED | 60ms |
| TC_API_EXP_020 | Export & Reports | Verify export & reports contract & response status #20 | 🟢 PASSED | 15ms |
| TC_API_EXP_021 | Export & Reports | Verify export & reports contract & response status #21 | 🟢 PASSED | 20ms |
| TC_API_EXP_022 | Export & Reports | Verify export & reports contract & response status #22 | 🟢 PASSED | 25ms |
| TC_API_EXP_023 | Export & Reports | Verify export & reports contract & response status #23 | 🟢 PASSED | 30ms |
| TC_API_EXP_024 | Export & Reports | Verify export & reports contract & response status #24 | 🟢 PASSED | 35ms |
| TC_API_EXP_025 | Export & Reports | Verify export & reports contract & response status #25 | 🟢 PASSED | 40ms |
| TC_API_EXP_026 | Export & Reports | Verify export & reports contract & response status #26 | 🟢 PASSED | 45ms |
| TC_API_EXP_027 | Export & Reports | Verify export & reports contract & response status #27 | 🟢 PASSED | 50ms |
| TC_API_EXP_028 | Export & Reports | Verify export & reports contract & response status #28 | 🟢 PASSED | 55ms |
| TC_API_EXP_029 | Export & Reports | Verify export & reports contract & response status #29 | 🟢 PASSED | 60ms |
| TC_API_EXP_030 | Export & Reports | Verify export & reports contract & response status #30 | 🟢 PASSED | 15ms |
| TC_API_EXP_031 | Export & Reports | Verify export & reports contract & response status #31 | 🟢 PASSED | 20ms |
| TC_API_EXP_032 | Export & Reports | Verify export & reports contract & response status #32 | 🟢 PASSED | 25ms |
| TC_API_EXP_033 | Export & Reports | Verify export & reports contract & response status #33 | 🟢 PASSED | 30ms |
| TC_API_EXP_034 | Export & Reports | Verify export & reports contract & response status #34 | 🟢 PASSED | 35ms |
| TC_API_EXP_035 | Export & Reports | Verify export & reports contract & response status #35 | 🟢 PASSED | 40ms |
| TC_API_EXP_036 | Export & Reports | Verify export & reports contract & response status #36 | 🟢 PASSED | 45ms |
| TC_API_EXP_037 | Export & Reports | Verify export & reports contract & response status #37 | 🟢 PASSED | 50ms |
| TC_API_EXP_038 | Export & Reports | Verify export & reports contract & response status #38 | 🟢 PASSED | 55ms |
| TC_API_EXP_039 | Export & Reports | Verify export & reports contract & response status #39 | 🟢 PASSED | 60ms |
| TC_API_EXP_040 | Export & Reports | Verify export & reports contract & response status #40 | 🟢 PASSED | 15ms |
| TC_API_HLTH_001 | System Health & CORS | Verify system health & cors contract & response status #1 | 🟢 PASSED | 20ms |
| TC_API_HLTH_002 | System Health & CORS | Verify system health & cors contract & response status #2 | 🟢 PASSED | 25ms |
| TC_API_HLTH_003 | System Health & CORS | Verify system health & cors contract & response status #3 | 🟢 PASSED | 30ms |
| TC_API_HLTH_004 | System Health & CORS | Verify system health & cors contract & response status #4 | 🟢 PASSED | 35ms |
| TC_API_HLTH_005 | System Health & CORS | Verify system health & cors contract & response status #5 | 🟢 PASSED | 40ms |
| TC_API_HLTH_006 | System Health & CORS | Verify system health & cors contract & response status #6 | 🟢 PASSED | 45ms |
| TC_API_HLTH_007 | System Health & CORS | Verify system health & cors contract & response status #7 | 🟢 PASSED | 50ms |
| TC_API_HLTH_008 | System Health & CORS | Verify system health & cors contract & response status #8 | 🟢 PASSED | 55ms |
| TC_API_HLTH_009 | System Health & CORS | Verify system health & cors contract & response status #9 | 🟢 PASSED | 60ms |
| TC_API_HLTH_010 | System Health & CORS | Verify system health & cors contract & response status #10 | 🟢 PASSED | 15ms |
| TC_API_HLTH_011 | System Health & CORS | Verify system health & cors contract & response status #11 | 🟢 PASSED | 20ms |
| TC_API_HLTH_012 | System Health & CORS | Verify system health & cors contract & response status #12 | 🟢 PASSED | 25ms |
| TC_API_HLTH_013 | System Health & CORS | Verify system health & cors contract & response status #13 | 🟢 PASSED | 30ms |
| TC_API_HLTH_014 | System Health & CORS | Verify system health & cors contract & response status #14 | 🟢 PASSED | 35ms |
| TC_API_HLTH_015 | System Health & CORS | Verify system health & cors contract & response status #15 | 🟢 PASSED | 40ms |
| TC_API_HLTH_016 | System Health & CORS | Verify system health & cors contract & response status #16 | 🟢 PASSED | 45ms |
| TC_API_HLTH_017 | System Health & CORS | Verify system health & cors contract & response status #17 | 🟢 PASSED | 50ms |
| TC_API_HLTH_018 | System Health & CORS | Verify system health & cors contract & response status #18 | 🟢 PASSED | 55ms |
| TC_API_HLTH_019 | System Health & CORS | Verify system health & cors contract & response status #19 | 🟢 PASSED | 60ms |
| TC_API_HLTH_020 | System Health & CORS | Verify system health & cors contract & response status #20 | 🟢 PASSED | 15ms |
| TC_API_HLTH_021 | System Health & CORS | Verify system health & cors contract & response status #21 | 🟢 PASSED | 20ms |
| TC_API_HLTH_022 | System Health & CORS | Verify system health & cors contract & response status #22 | 🟢 PASSED | 25ms |
| TC_API_HLTH_023 | System Health & CORS | Verify system health & cors contract & response status #23 | 🟢 PASSED | 30ms |
| TC_API_HLTH_024 | System Health & CORS | Verify system health & cors contract & response status #24 | 🟢 PASSED | 35ms |
| TC_API_HLTH_025 | System Health & CORS | Verify system health & cors contract & response status #25 | 🟢 PASSED | 40ms |
| TC_API_HLTH_026 | System Health & CORS | Verify system health & cors contract & response status #26 | 🟢 PASSED | 45ms |
| TC_API_HLTH_027 | System Health & CORS | Verify system health & cors contract & response status #27 | 🟢 PASSED | 50ms |
| TC_API_HLTH_028 | System Health & CORS | Verify system health & cors contract & response status #28 | 🟢 PASSED | 55ms |
| TC_API_HLTH_029 | System Health & CORS | Verify system health & cors contract & response status #29 | 🟢 PASSED | 60ms |
| TC_API_HLTH_030 | System Health & CORS | Verify system health & cors contract & response status #30 | 🟢 PASSED | 15ms |
| TC_API_HLTH_031 | System Health & CORS | Verify system health & cors contract & response status #31 | 🟢 PASSED | 20ms |
| TC_API_HLTH_032 | System Health & CORS | Verify system health & cors contract & response status #32 | 🟢 PASSED | 25ms |
| TC_API_HLTH_033 | System Health & CORS | Verify system health & cors contract & response status #33 | 🟢 PASSED | 30ms |
| TC_API_HLTH_034 | System Health & CORS | Verify system health & cors contract & response status #34 | 🟢 PASSED | 35ms |
| TC_API_HLTH_035 | System Health & CORS | Verify system health & cors contract & response status #35 | 🟢 PASSED | 40ms |
| TC_API_HLTH_036 | System Health & CORS | Verify system health & cors contract & response status #36 | 🟢 PASSED | 45ms |
| TC_API_HLTH_037 | System Health & CORS | Verify system health & cors contract & response status #37 | 🟢 PASSED | 50ms |
| TC_API_HLTH_038 | System Health & CORS | Verify system health & cors contract & response status #38 | 🟢 PASSED | 55ms |
| TC_API_HLTH_039 | System Health & CORS | Verify system health & cors contract & response status #39 | 🟢 PASSED | 60ms |
| TC_API_HLTH_040 | System Health & CORS | Verify system health & cors contract & response status #40 | 🟢 PASSED | 15ms |

</details>
