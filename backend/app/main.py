from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.logging import configure_logging
from app.config.settings import settings
from app.routers import admin, admin_mfa, admin_users, audit, auth, content, documents, eligibility, files, master_data, notifications, patient_auth, patients, policies, schemes, uploads
from app.utils.audit_middleware import audit_middleware
from app.utils.db_init import ensure_indexes


def create_app() -> FastAPI:
    configure_logging()

    app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_PREFIX}/openapi.json")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Add audit middleware for logging write operations
    app.middleware("http")(audit_middleware)

    app.include_router(auth.router, prefix=settings.API_PREFIX)
    app.include_router(policies.router, prefix=settings.API_PREFIX)
    app.include_router(uploads.router, prefix=settings.API_PREFIX)
    app.include_router(admin.router, prefix=settings.API_PREFIX)
    app.include_router(admin_users.router, prefix=settings.API_PREFIX)
    app.include_router(admin_mfa.router, prefix=settings.API_PREFIX)
    app.include_router(audit.router, prefix=settings.API_PREFIX)
    app.include_router(content.router, prefix=settings.API_PREFIX)
    app.include_router(master_data.router, prefix=settings.API_PREFIX)
    app.include_router(patient_auth.router, prefix=settings.API_PREFIX)
    app.include_router(patients.router, prefix=settings.API_PREFIX)
    app.include_router(documents.router, prefix=settings.API_PREFIX)
    app.include_router(schemes.router, prefix=settings.API_PREFIX)
    app.include_router(eligibility.router, prefix=settings.API_PREFIX)
    app.include_router(files.router, prefix=settings.API_PREFIX)
    app.include_router(notifications.router, prefix=settings.API_PREFIX)

    @app.on_event("startup")
    async def startup_event():
        await ensure_indexes()

    @app.get("/healthz")
    async def healthz():
        return {"status": "ok"}

    return app


app = create_app()
