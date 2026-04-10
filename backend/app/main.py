from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.logging import configure_logging
from app.config.settings import settings
from app.routers import admin, auth, policies, uploads
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

    app.include_router(auth.router, prefix=settings.API_PREFIX)
    app.include_router(policies.router, prefix=settings.API_PREFIX)
    app.include_router(uploads.router, prefix=settings.API_PREFIX)
    app.include_router(admin.router, prefix=settings.API_PREFIX)

    @app.on_event("startup")
    async def startup_event():
        await ensure_indexes()

    @app.get("/healthz")
    async def healthz():
        return {"status": "ok"}

    return app


app = create_app()
