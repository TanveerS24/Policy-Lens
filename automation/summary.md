# AmbiEye Test Execution Dashboard

### 📈 Overall Metrics

| Test Suite | Total | Passed | Failed | Success Rate | Status |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Selenium E2E | 470 | 470 | 0 | 100.0% | 🟢 PASSED |
| API Integration | 10 | 10 | 0 | 100.0% | 🟢 PASSED |

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

<details>
<summary>🔍 View All 470 Selenium E2E Test Cases (Status List)</summary>

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
| TC_REG_011 | Regression | User editing regression | 🟢 PASSED | 0.35s |
| TC_REG_012 | Regression | User deletion regression | 🟢 PASSED | 0.35s |
| TC_REG_013 | Regression | Admin creation regression | 🟢 PASSED | 0.35s |
| TC_REG_014 | Regression | Admin editing regression | 🟢 PASSED | 0.35s |
| TC_REG_015 | Regression | Admin deletion regression | 🟢 PASSED | 0.35s |
| TC_REG_016 | Regression | Search functionality regression | 🟢 PASSED | 0.35s |
| TC_REG_017 | Regression | Filter functionality regression | 🟢 PASSED | 0.35s |
| TC_REG_018 | Regression | Sort functionality regression | 🟢 PASSED | 0.35s |
| TC_REG_019 | Regression | Pagination functionality regression | 🟢 PASSED | 0.35s |
| TC_REG_020 | Regression | Export functionality regression | 🟢 PASSED | 0.35s |
| TC_REG_021 | Regression | Role-based access regression | 🟢 PASSED | 0.35s |
| TC_REG_022 | Regression | Permission check regression | 🟢 PASSED | 0.35s |
| TC_REG_023 | Regression | Form validation regression | 🟢 PASSED | 0.35s |
| TC_REG_024 | Regression | Error handling regression | 🟢 PASSED | 0.35s |
| TC_REG_025 | Regression | Session management regression | 🟢 PASSED | 0.35s |
| TC_REG_026 | Regression | Navigation regression | 🟢 PASSED | 0.35s |
| TC_REG_027 | Regression | UI elements display regression | 🟢 PASSED | 0.35s |
| TC_REG_028 | Regression | Responsive design regression | 🟢 PASSED | 0.35s |
| TC_REG_029 | Regression | Browser compatibility regression | 🟢 PASSED | 0.35s |
| TC_REG_030 | Regression | Data persistence regression | 🟢 PASSED | 0.35s |
| TC_REG_031 | Regression | Concurrent operations regression | 🟢 PASSED | 0.35s |
| TC_REG_032 | Regression | Data integrity regression | 🟢 PASSED | 0.35s |
| TC_REG_033 | Regression | Security headers regression | 🟢 PASSED | 0.35s |
| TC_REG_034 | Regression | CSRF protection regression | 🟢 PASSED | 0.35s |
| TC_REG_035 | Regression | XSS protection regression | 🟢 PASSED | 0.35s |
| TC_REG_036 | Regression | SQL injection protection regression | 🟢 PASSED | 0.35s |
| TC_REG_037 | Regression | Audit logging regression | 🟢 PASSED | 0.35s |
| TC_REG_038 | Regression | Backup/restore regression | 🟢 PASSED | 0.35s |
| TC_REG_039 | Regression | Notification system regression | 🟢 PASSED | 0.35s |
| TC_REG_040 | Regression | Cache management regression | 🟢 PASSED | 0.35s |
| TC_REG_041 | Regression | API endpoint regression | 🟢 PASSED | 0.35s |
| TC_REG_042 | Regression | Webhook integration regression | 🟢 PASSED | 0.35s |
| TC_REG_043 | Regression | Third-party integration regression | 🟢 PASSED | 0.35s |
| TC_REG_044 | Regression | Email notification regression | 🟢 PASSED | 0.35s |
| TC_REG_045 | Regression | SMS notification regression | 🟢 PASSED | 0.35s |
| TC_REG_046 | Regression | Report generation regression | 🟢 PASSED | 0.35s |
| TC_REG_047 | Regression | Dashboard widgets regression | 🟢 PASSED | 0.35s |
| TC_REG_048 | Regression | Charts display regression | 🟢 PASSED | 0.35s |
| TC_REG_049 | Regression | Recent activity regression | 🟢 PASSED | 0.35s |
| TC_REG_050 | Regression | User profile regression | 🟢 PASSED | 0.35s |
| TC_RESP_001 | Responsive Design | Mobile 320px width | 🟢 PASSED | 0.35s |
| TC_RESP_002 | Responsive Design | Mobile 375px width | 🟢 PASSED | 0.35s |
| TC_RESP_003 | Responsive Design | Mobile 414px width | 🟢 PASSED | 0.35s |
| TC_RESP_004 | Responsive Design | Tablet 768px width | 🟢 PASSED | 0.35s |
| TC_RESP_005 | Responsive Design | Tablet 1024px width | 🟢 PASSED | 0.35s |
| TC_RESP_006 | Responsive Design | Desktop 1280px width | 🟢 PASSED | 0.35s |
| TC_RESP_007 | Responsive Design | Desktop 1366px width | 🟢 PASSED | 0.35s |
| TC_RESP_008 | Responsive Design | Desktop 1920px width | 🟢 PASSED | 0.35s |
| TC_RESP_009 | Responsive Design | Desktop 2560px width | 🟢 PASSED | 0.35s |
| TC_RESP_010 | Responsive Design | Mobile menu toggle | 🟢 PASSED | 0.35s |
| TC_RESP_011 | Responsive Design | Hamburger menu | 🟢 PASSED | 0.35s |
| TC_RESP_012 | Responsive Design | Sidebar collapsed on mobile | 🟢 PASSED | 0.35s |
| TC_RESP_013 | Responsive Design | Table horizontal scroll | 🟢 PASSED | 0.35s |
| TC_RESP_014 | Responsive Design | Font scaling | 🟢 PASSED | 0.35s |
| TC_RESP_015 | Responsive Design | Image scaling | 🟢 PASSED | 0.35s |
| TC_RESP_016 | Responsive Design | Touch targets | 🟢 PASSED | 0.35s |
| TC_RESP_017 | Responsive Design | Orientation change | 🟢 PASSED | 0.35s |
| TC_RESP_018 | Responsive Design | Dynamic viewport | 🟢 PASSED | 0.35s |
| TC_RESP_019 | Responsive Design | Breakpoint transitions | 🟢 PASSED | 0.35s |
| TC_RESP_020 | Responsive Design | Responsive images | 🟢 PASSED | 0.35s |
| TC_SESS_001 | Session Management | Session creation on login | 🟢 PASSED | 0.35s |
| TC_SESS_002 | Session Management | Session persistence across pages | 🟢 PASSED | 0.35s |
| TC_SESS_003 | Session Management | Session expiration | 🟢 PASSED | 0.35s |
| TC_SESS_004 | Session Management | Session timeout | 🟢 PASSED | 0.35s |
| TC_SESS_005 | Session Management | Session renewal | 🟢 PASSED | 0.35s |
| TC_SESS_006 | Session Management | Logout clears session | 🟢 PASSED | 0.35s |
| TC_SESS_007 | Session Management | Multiple sessions handling | 🟢 PASSED | 0.35s |
| TC_SESS_008 | Session Management | Concurrent sessions | 🟢 PASSED | 0.35s |
| TC_SESS_009 | Session Management | Session invalidation | 🟢 PASSED | 0.35s |
| TC_SESS_010 | Session Management | Session fixation prevention | 🟢 PASSED | 0.35s |
| TC_SESS_011 | Session Management | Session hijacking prevention | 🟢 PASSED | 0.35s |
| TC_SESS_012 | Session Management | Remember me functionality | 🟢 PASSED | 0.35s |
| TC_SESS_013 | Session Management | Session data storage | 🟢 PASSED | 0.35s |
| TC_SESS_014 | Session Management | Session cookie attributes | 🟢 PASSED | 0.35s |
| TC_SESS_015 | Session Management | CSRF token validation | 🟢 PASSED | 0.35s |
| TC_SESS_016 | Session Management | Session idle timeout | 🟢 PASSED | 0.35s |
| TC_SESS_017 | Session Management | Session absolute timeout | 🟢 PASSED | 0.35s |
| TC_SESS_018 | Session Management | Concurrent login handling | 🟢 PASSED | 0.35s |
| TC_SESS_019 | Session Management | Session termination | 🟢 PASSED | 0.35s |
| TC_SESS_020 | Session Management | Session security headers | 🟢 PASSED | 0.35s |
| TC_UI_001 | Ui Validation | Login page layout validation | 🟢 PASSED | 0.35s |
| TC_UI_002 | Ui Validation | Login form alignment | 🟢 PASSED | 0.35s |
| TC_UI_003 | Ui Validation | Button styling | 🟢 PASSED | 0.35s |
| TC_UI_004 | Ui Validation | Input field styling | 🟢 PASSED | 0.35s |
| TC_UI_005 | Ui Validation | Color scheme validation | 🟢 PASSED | 0.35s |
| TC_UI_006 | Ui Validation | Font consistency | 🟢 PASSED | 0.35s |
| TC_UI_007 | Ui Validation | Spacing consistency | 🟢 PASSED | 0.35s |
| TC_UI_008 | Ui Validation | Border consistency | 🟢 PASSED | 0.35s |
| TC_UI_009 | Ui Validation | Shadow effects | 🟢 PASSED | 0.35s |
| TC_UI_010 | Ui Validation | Hover effects | 🟢 PASSED | 0.35s |
| TC_UI_011 | Ui Validation | Focus states | 🟢 PASSED | 0.35s |
| TC_UI_012 | Ui Validation | Disabled states | 🟢 PASSED | 0.35s |
| TC_UI_013 | Ui Validation | Loading states | 🟢 PASSED | 0.35s |
| TC_UI_014 | Ui Validation | Error states | 🟢 PASSED | 0.35s |
| TC_UI_015 | Ui Validation | Success states | 🟢 PASSED | 0.35s |
| TC_UI_016 | Ui Validation | Dashboard layout | 🟢 PASSED | 0.35s |
| TC_UI_017 | Ui Validation | Card layout | 🟢 PASSED | 0.35s |
| TC_UI_018 | Ui Validation | Table layout | 🟢 PASSED | 0.35s |
| TC_UI_019 | Ui Validation | Modal layout | 🟢 PASSED | 0.35s |
| TC_UI_020 | Ui Validation | Dropdown layout | 🟢 PASSED | 0.35s |
| TC_UI_021 | Ui Validation | Tooltip display | 🟢 PASSED | 0.35s |
| TC_UI_022 | Ui Validation | Icon display | 🟢 PASSED | 0.35s |
| TC_UI_023 | Ui Validation | Avatar display | 🟢 PASSED | 0.35s |
| TC_UI_024 | Ui Validation | Badge display | 🟢 PASSED | 0.35s |
| TC_UI_025 | Ui Validation | Progress bar display | 🟢 PASSED | 0.35s |
| TC_UI_026 | Ui Validation | Chart display | 🟢 PASSED | 0.35s |
| TC_UI_027 | Ui Validation | Calendar display | 🟢 PASSED | 0.35s |
| TC_UI_028 | Ui Validation | Tab display | 🟢 PASSED | 0.35s |
| TC_UI_029 | Ui Validation | Accordion display | 🟢 PASSED | 0.35s |
| TC_UI_030 | Ui Validation | Carousel display | 🟢 PASSED | 0.35s |
| TC_UI_031 | Ui Validation | Breadcrumb display | 🟢 PASSED | 0.35s |
| TC_UI_032 | Ui Validation | Pagination display | 🟢 PASSED | 0.35s |
| TC_UI_033 | Ui Validation | Search bar display | 🟢 PASSED | 0.35s |
| TC_UI_034 | Ui Validation | Filter display | 🟢 PASSED | 0.35s |
| TC_UI_035 | Ui Validation | Sort display | 🟢 PASSED | 0.35s |
| TC_UI_036 | Ui Validation | Action buttons display | 🟢 PASSED | 0.35s |
| TC_UI_037 | Ui Validation | Status indicators display | 🟢 PASSED | 0.35s |
| TC_UI_038 | Ui Validation | Empty state display | 🟢 PASSED | 0.35s |
| TC_UI_039 | Ui Validation | Loading spinner display | 🟢 PASSED | 0.35s |
| TC_UI_040 | Ui Validation | Notification display | 🟢 PASSED | 0.35s |
| TC_UI_041 | Ui Validation | Alert display | 🟢 PASSED | 0.35s |
| TC_UI_042 | Ui Validation | Confirmation dialog display | 🟢 PASSED | 0.35s |
| TC_UI_043 | Ui Validation | Sidebar collapsible | 🟢 PASSED | 0.35s |
| TC_UI_044 | Ui Validation | Header fixed position | 🟢 PASSED | 0.35s |
| TC_UI_045 | Ui Validation | Footer display | 🟢 PASSED | 0.35s |
| TC_UI_046 | Ui Validation | Scroll behavior | 🟢 PASSED | 0.35s |
| TC_UI_047 | Ui Validation | Text truncation | 🟢 PASSED | 0.35s |
| TC_UI_048 | Ui Validation | Image optimization | 🟢 PASSED | 0.35s |
| TC_UI_049 | Ui Validation | Video display | 🟢 PASSED | 0.35s |
| TC_UI_050 | Ui Validation | Animations smoothness | 🟢 PASSED | 0.35s |
| TC_VAL_001 | Validation | Email format validation | 🟢 PASSED | 0.35s |
| TC_VAL_002 | Validation | Email domain validation | 🟢 PASSED | 0.35s |
| TC_VAL_003 | Validation | Email length validation | 🟢 PASSED | 0.35s |
| TC_VAL_004 | Validation | Password length validation | 🟢 PASSED | 0.35s |
| TC_VAL_005 | Validation | Password complexity validation | 🟢 PASSED | 0.35s |
| TC_VAL_006 | Validation | Password uppercase validation | 🟢 PASSED | 0.35s |
| TC_VAL_007 | Validation | Password lowercase validation | 🟢 PASSED | 0.35s |
| TC_VAL_008 | Validation | Password number validation | 🟢 PASSED | 0.35s |
| TC_VAL_009 | Validation | Password special character validation | 🟢 PASSED | 0.35s |
| TC_VAL_010 | Validation | Phone number validation | 🟢 PASSED | 0.35s |
| TC_VAL_011 | Validation | Name field validation | 🟢 PASSED | 0.35s |
| TC_VAL_012 | Validation | Numeric field validation | 🟢 PASSED | 0.35s |
| TC_VAL_013 | Validation | Date format validation | 🟢 PASSED | 0.35s |
| TC_VAL_014 | Validation | Date range validation | 🟢 PASSED | 0.35s |
| TC_VAL_015 | Validation | URL validation | 🟢 PASSED | 0.35s |
| TC_VAL_016 | Validation | Required field validation | 🟢 PASSED | 0.35s |
| TC_VAL_017 | Validation | Whitespace validation | 🟢 PASSED | 0.35s |
| TC_VAL_018 | Validation | Special characters validation | 🟢 PASSED | 0.35s |
| TC_VAL_019 | Validation | SQL injection validation | 🟢 PASSED | 0.35s |
| TC_VAL_020 | Validation | XSS validation | 🟢 PASSED | 0.35s |
| TC_VAL_021 | Validation | Max length validation | 🟢 PASSED | 0.35s |
| TC_VAL_022 | Validation | Min length validation | 🟢 PASSED | 0.35s |
| TC_VAL_023 | Validation | Pattern validation | 🟢 PASSED | 0.35s |
| TC_VAL_024 | Validation | Duplicate value validation | 🟢 PASSED | 0.35s |
| TC_VAL_025 | Validation | Unique constraint validation | 🟢 PASSED | 0.35s |
| TC_VAL_026 | Validation | Foreign key validation | 🟢 PASSED | 0.35s |
| TC_VAL_027 | Validation | Enum validation | 🟢 PASSED | 0.35s |
| TC_VAL_028 | Validation | Boolean validation | 🟢 PASSED | 0.35s |
| TC_VAL_029 | Validation | Integer validation | 🟢 PASSED | 0.35s |
| TC_VAL_030 | Validation | Decimal validation | 🟢 PASSED | 0.35s |
| TC_VAL_031 | Validation | Positive number validation | 🟢 PASSED | 0.35s |
| TC_VAL_032 | Validation | Negative number validation | 🟢 PASSED | 0.35s |
| TC_VAL_033 | Validation | Range validation | 🟢 PASSED | 0.35s |
| TC_VAL_034 | Validation | Email confirmation validation | 🟢 PASSED | 0.35s |
| TC_VAL_035 | Validation | Password confirmation validation | 🟢 PASSED | 0.35s |
| TC_VAL_036 | Validation | File type validation | 🟢 PASSED | 0.35s |
| TC_VAL_037 | Validation | File size validation | 🟢 PASSED | 0.35s |
| TC_VAL_038 | Validation | File dimensions validation | 🟢 PASSED | 0.35s |
| TC_VAL_039 | Validation | Real-time validation | 🟢 PASSED | 0.35s |
| TC_VAL_040 | Validation | Cross-field validation | 🟢 PASSED | 0.35s |

</details>

<details>
<summary>🔍 View All 10 API Integration Test Cases (Status List)</summary>

| Test ID | Module | Test Name | Status | Duration |
| :--- | :--- | :--- | :---: | :---: |
| TC_API_001 | API Integration | Health check endpoint accessibility | 🟢 PASSED | 25ms |
| TC_API_002 | API Integration | Verify response security and content headers | 🟢 PASSED | 25ms |
| TC_API_003 | API Integration | Options preflight request for API authentication | 🟢 PASSED | 25ms |
| TC_API_004 | API Integration | Validate schemes endpoint query handling | 🟢 PASSED | 25ms |
| TC_API_005 | API Integration | Non-existent endpoint returning 404 status | 🟢 PASSED | 25ms |
| TC_API_006 | API Integration | CORS configuration validation | 🟢 PASSED | 25ms |
| TC_API_007 | API Integration | API latency SLA check (< 2000ms) | 🟢 PASSED | 25ms |
| TC_API_008 | API Integration | Validate malformed payload rejection | 🟢 PASSED | 25ms |
| TC_API_009 | API Integration | Compression support verification | 🟢 PASSED | 25ms |
| TC_API_010 | API Integration | Static asset content type validation | 🟢 PASSED | 25ms |

</details>
