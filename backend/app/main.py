"""FastAPI application entrypoint for the ARIP backend."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.health import router as health_router
from app.api.v1.upload import router as upload_router
from app.core.config import get_settings
from app.core.logger import configure_logging, get_logger

settings = get_settings()
configure_logging(settings)
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Handle application startup and shutdown events."""
    logger.info(
        "Starting {application} {version} in {environment} mode",
        application=settings.app_name,
        version=settings.app_version,
        environment=settings.environment,
    )
    yield
    logger.info("Shutting down {application}", application=settings.app_name)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance."""
    application = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        lifespan=lifespan,
    )
    application.include_router(health_router)
    application.include_router(health_router, prefix=settings.api_v1_prefix)
    application.include_router(upload_router, prefix=settings.api_v1_prefix)
    return application


app = create_app()
