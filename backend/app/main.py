"""Main FastAPI application entry point."""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import structlog
import time

from app.config.settings import get_settings
from app.api.v1.router import api_router
from app.config.database import engine, Base

logger = structlog.get_logger()
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: startup and shutdown logic."""
    # --- Startup ---
    logger.info("application_startup", app_name=settings.APP_NAME)
    Base.metadata.create_all(bind=engine)

    # Run safe migrations for new columns on existing tables
    from sqlalchemy import text, inspect
    try:
        with engine.connect() as conn:
            inspector = inspect(engine)
            existing_tables = inspector.get_table_names()
            if "schemes" in existing_tables:
                columns = [col["name"] for col in inspector.get_columns("schemes")]
                
                # Add missing columns for schemes
                migrations = [
                    ("full_document_text", "TEXT"),
                    ("original_document_path", "VARCHAR(500)"),
                    ("original_document_filename", "VARCHAR(255)"),
                ]
                
                for column_name, column_type in migrations:
                    if column_name not in columns:
                        conn.execute(
                            text(f"ALTER TABLE schemes ADD COLUMN {column_name} {column_type}")
                        )
                        conn.commit()
                        logger.info("migration_applied", column=column_name, table="schemes")

            if "documents" in existing_tables:
                doc_columns = [col["name"] for col in inspector.get_columns("documents")]
                doc_migrations = [
                    ("publish_status", "VARCHAR(30) DEFAULT 'draft'"),
                    ("publish_requested", "BOOLEAN DEFAULT FALSE"),
                    ("publish_requested_at", "TIMESTAMP WITH TIME ZONE"),
                ]
                for col_name, col_type in doc_migrations:
                    if col_name not in doc_columns:
                        conn.execute(
                            text(f"ALTER TABLE documents ADD COLUMN {col_name} {col_type}")
                        )
                        conn.commit()
                        logger.info("migration_applied", column=col_name, table="documents")

            if "ai_summaries" in existing_tables:
                ai_columns = [col["name"] for col in inspector.get_columns("ai_summaries")]
                if "eligibility_criteria" not in ai_columns:
                    conn.execute(
                        text("ALTER TABLE ai_summaries ADD COLUMN eligibility_criteria TEXT")
                    )
                    conn.commit()
                    logger.info("migration_applied", column="eligibility_criteria", table="ai_summaries")
    except Exception as exc:
        logger.error("startup_migration_failed", error=str(exc))

    yield

    # --- Shutdown ---
    logger.info("application_shutdown", app_name=settings.APP_NAME)


def create_application() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title=settings.APP_NAME,
        description="Policy Lens — Policy Management Platform",
        version="1.0.0",
        docs_url="/api/docs" if settings.DEBUG else None,
        redoc_url="/api/redoc" if settings.DEBUG else None,
        lifespan=lifespan,
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Trusted host middleware
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.ALLOWED_HOSTS,
    )

    # Request logging middleware
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time

        logger.info(
            "request_completed",
            method=request.method,
            path=request.url.path,
            status=response.status_code,
            duration_ms=round(duration * 1000, 2),
        )
        return response

    # Include API router
    app.include_router(api_router, prefix="/api/v1")

    # Exception handlers
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        logger.error(
            "validation_error",
            details=str(exc.errors()),
            body=str(exc.body) if hasattr(exc, "body") else None,
            path=request.url.path,
        )
        return JSONResponse(
            status_code=422,
            content={
                "error": "Validation failed",
                "details": str(exc.errors()),
            },
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error("unhandled_exception", error=str(exc), path=request.url.path)
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error"},
        )

    return app


app = create_application()


@app.get("/health")
@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "1.0.0"}
