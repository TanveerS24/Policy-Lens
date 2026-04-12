# DentalSchemes India - PRD Implementation Gap Analysis

## Executive Summary

The current codebase (Policy-Lens) is a generic policy management system that requires significant restructuring to meet the DentalSchemes India PRD requirements. The current implementation uses email/password authentication, while the PRD requires mobile-based OTP authentication. The data models, user roles, and feature sets are substantially different.

---

## Critical Gaps Analysis

### 1. Authentication System (CRITICAL - Complete Rewrite Required)

**PRD Requirements:**
- Primary identifier: Mobile number (10 digits, starts with 6-9)
- 6-digit OTP via SMS for verification
- OTP expiry: 10 minutes
- Max attempts per OTP: 3
- Max OTP requests per hour: 5
- Account lockout after 5 failed login attempts (30 minutes)
- JWT with RS256, access token 1 hour, refresh token 30 days
- Forgot password via mobile OTP

**Current Implementation:**
- Email/password based authentication
- Basic OTP for email verification only
- No rate limiting on OTP
- No account lockout mechanism
- JWT with simple signing
- No forgot password flow

**Impact:** Complete authentication system rewrite required

---

### 2. Patient Registration (CRITICAL - Major Changes Required)

**PRD Required Fields:**
- Full Name (2-100 chars, alphabets and spaces only)
- Date of Birth (DD/MM/YYYY, must be in past, age 0-120)
- Gender (Male/Female/Transgender/Prefer not to say)
- Mobile Number (10 digits, starts with 6-9, OTP verified)
- Email Address (optional, standard email regex)
- State (dropdown from master list)
- District (dropdown dependent on state)
- Pin Code (6 digits, validated against state-district mapping)
- Password (min 8 chars, 1 uppercase, 1 lowercase, 1 digit, 1 special char)
- Confirm Password (must match)
- Terms & Conditions checkbox

**Current Implementation:**
- Name, email, password, age, gender, state, income
- No DOB field
- No district/pin code
- No mobile number
- No OTP verification
- No password complexity validation
- No terms checkbox

**Impact:** Registration form and backend validation complete rewrite

---

### 3. Patient Profile Management (HIGH - Not Implemented)

**PRD Requirements:**
- Profile view and edit
- Mobile number change with OTP re-verification
- Email verification on update
- Profile photo upload (JPEG/PNG, max 2MB, 1:1 ratio)
- Password change with current password
- Notification preferences (SMS and push toggles)
- Account deactivation (soft-delete, 90-day retention)
- Account deletion (permanent, DPDP compliance)
- Download My Data (export as ZIP)

**Current Implementation:**
- Not implemented

**Impact:** New feature implementation required

---

### 4. Dental Schemes Data Model (CRITICAL - Complete Rewrite Required)

**PRD Required Fields:**
- Scheme ID (UUID, auto-generated)
- Scheme Name (3-200 chars, unique per state)
- Scheme Type (National/State)
- State (dropdown, null for national schemes)
- Sponsoring Ministry/Dept (max 200 chars)
- Launch Date (cannot be future)
- Active Status (Active/Inactive/Discontinued)
- Short Description (50-500 chars)
- Detailed Description (rich text, max 5000 chars)
- Eligibility Criteria (rich text, max 3000 chars)
- Beneficiary Categories (multi-select tags: BPL/Senior Citizen/Child/Woman/Differently Abled/General)
- Income Ceiling (INR/year, optional, 0 = no limit)
- Age Group (Min-Max, 0-120)
- Services Covered (multi-select tags: Extraction/Filling/Scaling/Dentures/Orthodontics/X-Ray/Other)
- Coverage Amount (INR, optional, 0 = fully free)
- Enrolment Process (rich text, max 2000 chars)
- Required Documents (list, max 20 items)
- Helpline Number (10-digit or 1800 format)
- Official Website URL (HTTPS preferred)
- Reference Order/GO Number (max 100 chars)
- Last Updated By (admin user ID)
- Last Updated At (timestamp)

**Current Implementation:**
- Generic policy model with: title, short_description, summary, eligibility_criteria, benefits, notes, category, state, pdf_url
- No scheme-specific fields
- No version history
- No beneficiary categories
- No services covered
- No coverage amount
- No enrolment process

**Impact:** Complete data model rewrite with migration

---

### 5. Eligibility Criteria Module (CRITICAL - Complete Rewrite Required)

**PRD Requirements:**
- Structured JSON rules engine
- Supported operators: equals, not_equals, greater_than, less_than, in_list, not_in_list, range
- Rule fields: age, state, gender, income, beneficiary_category, disability_flag
- Admin rule builder (no raw JSON editing)
- Rule versioning with rollback
- Eligibility check flow with dynamic questions
- Results: Likely Eligible / Possibly Eligible / Not Eligible with reasons

**Current Implementation:**
- RAG-based eligibility check using LLM
- No structured rules
- No admin rule builder
- No version history

**Impact:** Complete rewrite of eligibility system

---

### 6. State & District Master Data (HIGH - Not Implemented)

**PRD Requirements:**
- State master: State Name, State Code, Capital City, Zone (North/South/East/West/Central/Northeast)
- District master: District Name, State (FK), STD Code, Pin Code range
- Both masters are append-only (no deletes, only deactivate)
- Changes trigger re-validation of patient addresses

**Current Implementation:**
- Not implemented
- State is a simple text field

**Impact:** New master data system required with seed data for 28 states + 8 UTs

---

### 7. Beneficiary Categories & Services Master (HIGH - Not Implemented)

**PRD Requirements:**
- Beneficiary Categories: Name, Code, Description, Icon
- Dental Services: Service Name, Code, Category (Preventive/Restorative/Surgical/Cosmetic)
- Used as dropdown/tag sources across scheme forms and eligibility checks

**Current Implementation:**
- Not implemented

**Impact:** New master data system required

---

### 8. Admin Roles & Permissions (CRITICAL - Complete Rewrite Required)

**PRD Requirements:**
- Super Admin: Full CRUD on all entities, manage admin users, view analytics
- Content Admin: CRUD on schemes and programs only
- Support Admin: View-only on user profiles, manage user queries
- Admin accounts created only by Super Admin
- MFA required (TOTP-based, e.g., Google Authenticator)
- Session timeout: 30 minutes
- Password policy: 12+ chars, change required every 90 days
- IP allowlisting configurable

**Current Implementation:**
- Simple is_admin boolean flag
- No role-based access control
- No MFA
- No session timeout
- No password policy enforcement

**Impact:** Complete RBAC system implementation required

---

### 9. Admin Dashboard (MEDIUM - Partial Implementation)

**PRD Requirements:**
- Total registered patients (today, this week, this month, total)
- Total active schemes (national vs state breakdown)
- Documents uploaded (last 30 days)
- AI summaries generated vs pending
- User activity heatmap
- Recent admin actions log (last 20 entries)
- System health indicators (API latency, storage usage, OTP delivery rate)

**Current Implementation:**
- Basic dashboard with: total_policies, pending_approvals, total_users, recent_policies
- No patient metrics
- No document metrics
- No AI summary metrics
- No activity heatmap
- No admin actions log
- No system health indicators

**Impact:** Dashboard enhancement required

---

### 10. Scheme Management Module (MEDIUM - Partial Implementation)

**PRD Requirements:**
- Full CRUD on schemes
- Bulk import via CSV template
- Bulk export as CSV or JSON
- Draft/Review/Published workflow
- Scheme change history with diff view
- Clone scheme functionality

**Current Implementation:**
- Basic CRUD on policies
- No bulk import/export
- No draft/review/published workflow (only approved boolean)
- No change history
- No clone functionality

**Impact:** Scheme management enhancement required

---

### 11. User Management Module (HIGH - Not Implemented)

**PRD Requirements:**
- Patient Accounts: View list, search by name/mobile/email, edit demographics, deactivate/reactivate, delete, view documents metadata, reset password
- Admin Account Management (Super Admin only): Create, edit, delete, role assignment, audit trail
- Role-specific permissions matrix

**Current Implementation:**
- Not implemented

**Impact:** New user management module required

---

### 12. Notification System (HIGH - Not Implemented)

**PRD Requirements:**
- Triggers: Registration, OTP, Password Change, Scheme Bookmarked, Document Upload, AI Summary Ready, New Scheme, Account Deactivation, Admin Action
- Channels: SMS, Push, Email
- Content templates per trigger
- Delivery status tracking

**Current Implementation:**
- Not implemented

**Impact:** Complete notification system required with SMS gateway integration

---

### 13. Document Upload & AI Summary (MEDIUM - Partial Implementation)

**PRD Requirements:**
- Accepted formats: PDF, JPG, PNG, TIFF
- Max file size: 10 MB
- Max documents per user: 20
- Cloud storage (AWS S3/GCP GCS)
- Virus scan before processing
- AI extracts: Coverage scope, Exclusions, Waiting periods, Premium/co-pay, Claim process, Renewal conditions, Grievance redressal
- Processing SLA: under 60 seconds
- Re-process limit: 3 per document
- Disclaimer: "AI-generated for informational purposes only"

**Current Implementation:**
- Basic PDF upload
- No file size limit
- No document limit per user
- No cloud storage
- No virus scan
- RAG-based Q&A instead of structured summary
- No processing SLA
- No re-process limit
- No disclaimer

**Impact:** Document system enhancement required

---

### 14. Content Management (MEDIUM - Not Implemented)

**PRD Requirements:**
- FAQ management: Question, Answer (rich text), Category, Sort Order, Active/Inactive
- Banner/Announcement management: Title, Body, Start Date, End Date, Target Audience, Platform
- Static pages: About, Privacy Policy, Terms (rich text with version history)

**Current Implementation:**
- Not implemented

**Impact:** New CMS module required

---

### 15. Audit Log (HIGH - Not Implemented)

**PRD Requirements:**
- Every write action logged
- Fields: actor_type, actor_id, action, entity_type, entity_id, before_json, after_json, ip, timestamp
- Viewable by Super Admin

**Current Implementation:**
- Not implemented

**Impact:** New audit logging system required

---

### 16. DPDP Compliance (HIGH - Not Implemented)

**PRD Requirements:**
- Data localization in Indian data centres
- 30-day cooling period for permanent deletion
- Data export functionality
- PII masking in logs

**Current Implementation:**
- Not implemented

**Impact:** Compliance features required

---

## API Endpoints Gap Analysis

### Missing Endpoints:
- POST /api/v1/auth/request-otp (mobile-based)
- POST /api/v1/auth/forgotpassword
- POST /api/v1/auth/resetpassword
- GET /api/v1/patients/me (patient profile)
- PATCH /api/v1/patients/me (update profile)
- DELETE /api/v1/patients/me (deactivate/delete)
- GET /api/v1/patients/me/documents
- POST /api/v1/patients/me/documents
- GET /api/v1/patients/me/documents/:id
- DELETE /api/v1/patients/me/documents/:id
- POST /api/v1/patients/me/documents/:id/reprocess
- GET /api/v1/schemes (with filters, pagination)
- POST /api/v1/schemes/:id/eligibility-check
- POST /api/v1/admin/schemes (create scheme)
- PUT /api/v1/admin/schemes/:id (update scheme)
- DELETE /api/v1/admin/schemes/:id (soft delete)
- POST /api/v1/admin/schemes/:id/publish
- Plus all user management, master data, CMS, notification endpoints

---

## Database Schema Changes Required

### Current Collections:
- users (basic user model)
- policies (generic policy model)

### Required New Collections:
- users (complete rewrite with patient fields)
- user_sessions
- user_otp_log
- states
- districts
- schemes (complete rewrite)
- scheme_versions
- eligibility_rules
- eligibility_checks
- documents
- document_summaries
- admin_users
- audit_log
- notifications
- beneficiary_categories
- dental_services
- cms_faqs
- cms_banners

---

## Technology Stack Changes

### Current Stack:
- Backend: FastAPI, MongoDB, Redis
- Admin Frontend: React, TypeScript, Vite
- Mobile: React Native, Expo

### Required Additions:
- SMS Gateway (MSG91/Exotel)
- Cloud Storage (AWS S3/GCP GCS)
- TOTP Library (for admin MFA)
- Virus Scanner (ClamAV or cloud equivalent)
- LLM API (Claude/OpenAI for AI summaries)
- Push Notification Service (FCM/APNS)

---

## Implementation Priority

### Phase 1 - Foundation (Critical)
1. Rewrite authentication system (mobile + OTP)
2. Rewrite patient registration with all required fields
3. Implement State & District master data
4. Implement Beneficiary Categories & Services master
5. Rewrite Dental Schemes data model
6. Implement basic RBAC for admin roles

### Phase 2 - Core Features
7. Implement Eligibility Rules Engine
8. Implement Patient Profile Management
9. Implement Scheme Management (CRUD + versioning)
10. Implement Document Upload with AI Summary
11. Implement Audit Logging

### Phase 3 - Admin Features
12. Implement Admin Dashboard enhancements
13. Implement User Management Module
14. Implement Content Management (FAQ, Banners)
15. Implement Admin MFA

### Phase 4 - Notifications & Compliance
16. Implement Notification System
17. Implement DPDP Compliance features
18. Implement data export/deletion workflows

---

## Estimated Effort

This is a complete rewrite of significant portions of the application. Estimated effort:
- Backend: 4-6 weeks for core rewrite
- Admin Frontend: 3-4 weeks for enhancements
- Mobile App: 3-4 weeks for complete auth and profile rewrite
- Testing & Integration: 2-3 weeks

**Total: 12-17 weeks for full PRD compliance**

---

## Recommendations

Given the scope of changes required, I recommend:

1. **Confirm the direction**: Do you want to fully implement the PRD as specified, or adapt the current generic system to a dental schemes focus with a phased approach?

2. **Prioritize features**: Which features are must-have for v1.0 launch?

3. **Consider incremental delivery**: Implement Phase 1 first, then iterate based on feedback.

4. **Database migration strategy**: Plan for migrating any existing data to the new schema.

5. **Third-party integrations**: Secure credentials for SMS gateway, cloud storage, and LLM API before starting implementation.
