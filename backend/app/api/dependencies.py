"""Dependencies for FastAPI routers, orchestrators, and in-memory caches."""

from typing import Annotated

from fastapi import Depends

from app.application.dto.analysis_presenter import AnalysisPresenter
from app.application.orchestrator.agent_orchestrator import AgentOrchestrator
from app.application.orchestrator.analysis_result import AnalysisResult
from app.application.services.document_storage import (
    DocumentStorageApplicationService,
)
from app.core.config import Settings, get_settings
from app.infrastructure.storage.provider import FileSystemStorageProvider
from app.infrastructure.storage.storage_service import DocumentStorageService
from app.infrastructure.storage.validator import FileValidator

# In-memory store cache for completed/partial AnalysisResult runs
ANALYSIS_STORE: dict[str, AnalysisResult] = {}


def get_document_storage_service(
    settings: Annotated[Settings, Depends(get_settings)],
) -> DocumentStorageApplicationService:
    """Build the document storage application service."""
    validator = FileValidator(
        allowed_extensions=settings.allowed_upload_extensions,
        allowed_mime_types=settings.allowed_upload_mime_types,
        max_size_bytes=settings.max_upload_size_bytes,
    )
    provider = FileSystemStorageProvider(settings=settings)
    storage_service = DocumentStorageService(provider=provider, validator=validator)
    return DocumentStorageApplicationService(storage_service=storage_service)


def get_agent_orchestrator() -> AgentOrchestrator:
    """Dependency injection provider for the AgentOrchestrator."""
    return AgentOrchestrator()


def get_analysis_presenter() -> AnalysisPresenter:
    """Dependency injection provider for the AnalysisPresenter."""
    return AnalysisPresenter()
