"""API endpoints package."""

from app.api.v1.endpoints import auth, patients, schemes, eligibility, documents, admin, notifications

__all__ = [
    "auth",
    "patients",
    "schemes",
    "eligibility",
    "documents",
    "admin",
    "notifications",
]
