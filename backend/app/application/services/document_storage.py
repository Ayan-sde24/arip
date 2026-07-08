"""Application service for document upload workflows."""

from fastapi import UploadFile

from app.infrastructure.storage.interfaces import StorageService
from app.infrastructure.storage.models import FileMetadata


class DocumentStorageApplicationService:
    """Coordinate document upload requests with storage services."""

    def __init__(self, *, storage_service: StorageService) -> None:
        """Initialize the application service."""
        self._storage_service = storage_service

    async def store_resume(self, *, file: UploadFile) -> FileMetadata:
        """Read an uploaded resume and delegate storage."""
        content = await file.read()
        return self._storage_service.store_resume(
            original_filename=file.filename or "",
            mime_type=file.content_type or "",
            content=content,
        )

    async def store_job_description(self, *, file: UploadFile) -> FileMetadata:
        """Read an uploaded job description and delegate storage."""
        content = await file.read()
        return self._storage_service.store_job_description(
            original_filename=file.filename or "",
            mime_type=file.content_type or "",
            content=content,
        )
