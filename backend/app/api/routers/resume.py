"""Resume router for uploading resume files."""

from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from pydantic import BaseModel, ConfigDict, Field

from app.api.dependencies import get_document_storage_service
from app.application.services.document_storage import (
    DocumentStorageApplicationService,
)
from app.core.logger import get_logger
from app.infrastructure.storage.exceptions import (
    StorageProviderError,
    StorageValidationError,
)

router = APIRouter(prefix="/resume", tags=["resume"])
logger = get_logger(__name__)


class ResumeUploadResponse(BaseModel):
    """Payload response returned upon successful resume upload."""

    model_config = ConfigDict(frozen=True)

    file_id: str
    filename: str
    size: int = Field(ge=0)
    checksum: str
    status: str


@router.post(
    "/upload",
    response_model=ResumeUploadResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_resume(
    file: Annotated[UploadFile, File()],
    service: Annotated[
        DocumentStorageApplicationService,
        Depends(get_document_storage_service),
    ],
) -> ResumeUploadResponse:
    """Upload and parse/persist a candidate resume file."""
    try:
        metadata = await service.store_resume(file=file)
    except StorageValidationError as exc:
        logger.warning("Resume upload validation error: {error}", error=str(exc))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except StorageProviderError as exc:
        logger.exception("Resume upload storage provider error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Storage failure",
        ) from exc

    return ResumeUploadResponse(
        file_id=str(metadata.id),
        filename=metadata.original_filename,
        size=metadata.size,
        checksum=metadata.sha256,
        status="uploaded",
    )
