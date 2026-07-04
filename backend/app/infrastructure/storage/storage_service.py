"""Document storage service implementation."""

from datetime import UTC, datetime
from hashlib import sha256
from uuid import uuid4

from app.core.logger import get_logger
from app.infrastructure.storage.interfaces import StorageProvider
from app.infrastructure.storage.models import DocumentType, FileMetadata
from app.infrastructure.storage.validator import FileValidator

logger = get_logger(__name__)


class DocumentStorageService:
    """Validate and store documents through a storage provider."""

    def __init__(self, *, provider: StorageProvider, validator: FileValidator) -> None:
        """Initialize the service with provider and validator dependencies."""
        self._provider = provider
        self._validator = validator

    def store_resume(
        self,
        *,
        original_filename: str,
        mime_type: str,
        content: bytes,
    ) -> FileMetadata:
        """Validate and store a resume document."""
        return self.store_document(
            original_filename=original_filename,
            mime_type=mime_type,
            content=content,
            document_type=DocumentType.RESUME,
        )

    def store_job_description(
        self,
        *,
        original_filename: str,
        mime_type: str,
        content: bytes,
    ) -> FileMetadata:
        """Validate and store a job description document."""
        return self.store_document(
            original_filename=original_filename,
            mime_type=mime_type,
            content=content,
            document_type=DocumentType.JOB_DESCRIPTION,
        )

    def store_document(
        self,
        *,
        original_filename: str,
        mime_type: str,
        content: bytes,
        document_type: DocumentType,
    ) -> FileMetadata:
        """Validate, checksum, rename, and store a document."""
        logger.info(
            "Upload started for {filename} as {document_type}",
            filename=original_filename,
            document_type=document_type.value,
        )
        extension = self._validator.validate(
            filename=original_filename,
            mime_type=mime_type,
            size=len(content),
        )
        file_id = uuid4()
        checksum = sha256(content).hexdigest()
        logger.info("Checksum generated for {filename}", filename=original_filename)

        stored_filename = f"{file_id}.{extension}"
        storage_path = self._provider.save(
            document_type=document_type,
            stored_filename=stored_filename,
            content=content,
        )

        return FileMetadata(
            id=file_id,
            original_filename=original_filename,
            stored_filename=stored_filename,
            extension=extension,
            mime_type=mime_type,
            size=len(content),
            sha256=checksum,
            upload_time=datetime.now(UTC),
            document_type=document_type,
            storage_path=storage_path,
        )
