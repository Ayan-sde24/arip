"""Document upload API routes."""

from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from pydantic import BaseModel, ConfigDict, Field

from app.application.services.document_storage import DocumentStorageApplicationService
from app.core.config import Settings, get_settings
from app.core.logger import get_logger
from app.infrastructure.storage.exceptions import (
    StorageProviderError,
    StorageValidationError,
)
from app.infrastructure.storage.provider import FileSystemStorageProvider
from app.infrastructure.storage.storage_service import DocumentStorageService
from app.infrastructure.storage.validator import FileValidator

router = APIRouter(prefix="/upload", tags=["upload"])
logger = get_logger(__name__)


class UploadResponse(BaseModel):
    """Standard response returned after a successful upload."""

    model_config = ConfigDict(frozen=True)

    file_id: str
    filename: str
    size: int = Field(ge=0)
    checksum: str
    status: str


def get_document_storage_application_service(
    settings: Annotated[Settings, Depends(get_settings)],
) -> DocumentStorageApplicationService:
    """Build the document storage application service dependency."""
    validator = FileValidator(
        allowed_extensions=settings.allowed_upload_extensions,
        allowed_mime_types=settings.allowed_upload_mime_types,
        max_size_bytes=settings.max_upload_size_bytes,
    )
    provider = FileSystemStorageProvider(settings=settings)
    storage_service = DocumentStorageService(provider=provider, validator=validator)
    return DocumentStorageApplicationService(storage_service=storage_service)


@router.post(
    "/resume",
    response_model=UploadResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_resume(
    file: Annotated[UploadFile, File()],
    service: Annotated[
        DocumentStorageApplicationService,
        Depends(get_document_storage_application_service),
    ],
) -> UploadResponse:
    """Upload and store a resume document."""
    try:
        metadata = await service.store_resume(file=file)
    except StorageValidationError as exc:
        logger.warning(
            "Validation failure during resume upload: {error}",
            error=str(exc),
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except StorageProviderError as exc:
        logger.exception("Storage error during resume upload")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Storage failure",
        ) from exc

    return UploadResponse(
        file_id=str(metadata.id),
        filename=metadata.original_filename,
        size=metadata.size,
        checksum=metadata.sha256,
        status="uploaded",
    )
