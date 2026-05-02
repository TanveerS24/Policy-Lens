"""Main API router configuration."""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, patients, schemes, documents, admin, eligibility, notifications

api_router = APIRouter()

# Auth routes
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# Patient routes
api_router.include_router(patients.router, prefix="/patients", tags=["Patients"])

# Scheme routes
api_router.include_router(schemes.router, prefix="/schemes", tags=["Schemes"])

# Eligibility routes
api_router.include_router(eligibility.router, prefix="/eligibility", tags=["Eligibility"])

# Document routes
api_router.include_router(documents.router, prefix="/documents", tags=["Documents"])

# Notification routes
api_router.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])

# Admin routes
api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])
