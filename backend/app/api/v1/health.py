"""Health check endpoints for service monitoring."""

from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict

from app.core.config import get_settings

router = APIRouter(tags=["health"])


class HealthResponse(BaseModel):
    """Response returned by the health check endpoint."""

    model_config = ConfigDict(frozen=True)

    status: Literal["healthy"]
    application: str
    version: str
    environment: str


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Return the current application health status."""
    settings = get_settings()
    return HealthResponse(
        status="healthy",
        application=settings.app_name,
        version=settings.app_version,
        environment=settings.environment,
    )
