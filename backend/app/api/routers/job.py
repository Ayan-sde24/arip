"""Job Description router for uploading job description documents."""

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

router = APIRouter(prefix="/job", tags=["job"])
logger = get_logger(__name__)


class JobUploadResponse(BaseModel):
    """Payload response returned upon successful job description upload."""

    model_config = ConfigDict(frozen=True)

    file_id: str
    filename: str
    size: int = Field(ge=0)
    checksum: str
    status: str


@router.post(
    "/upload",
    response_model=JobUploadResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_job(
    file: Annotated[UploadFile, File()],
    service: Annotated[
        DocumentStorageApplicationService,
        Depends(get_document_storage_service),
    ],
) -> JobUploadResponse:
    """Upload and persist a job description file."""
    try:
        metadata = await service.store_job_description(file=file)
    except StorageValidationError as exc:
        logger.warning("Job upload validation error: {error}", error=str(exc))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except StorageProviderError as exc:
        logger.exception("Job upload storage provider error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Storage failure",
        ) from exc

    return JobUploadResponse(
        file_id=str(metadata.id),
        filename=metadata.original_filename,
        size=metadata.size,
        checksum=metadata.sha256,
        status="uploaded",
    )
