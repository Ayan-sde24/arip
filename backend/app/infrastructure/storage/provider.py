"""Filesystem implementation of the storage provider interface."""

from datetime import UTC, datetime
from pathlib import Path

from app.core.config import Settings
from app.core.logger import get_logger
from app.infrastructure.storage.exceptions import StorageProviderError
from app.infrastructure.storage.models import (
    DocumentType,
    StoredFileMetadata,
    normalize_storage_path,
)

logger = get_logger(__name__)


class FileSystemStorageProvider:
    """Persist documents to the local filesystem."""

    def __init__(self, *, settings: Settings) -> None:
        """Initialize the provider with configured storage locations."""
        self._base_path = settings.storage_root
        self._directories = {
            DocumentType.RESUME: settings.resume_upload_dir,
            DocumentType.JOB_DESCRIPTION: settings.job_upload_dir,
            DocumentType.DOCUMENT: settings.uploads_root / "documents",
        }

    def save(
        self,
        *,
        document_type: DocumentType,
        stored_filename: str,
        content: bytes,
    ) -> str:
        """Persist document bytes and return a relative storage path."""
        try:
            directory = self._directories[document_type]
            directory.mkdir(parents=True, exist_ok=True)
            target_path = directory / stored_filename
            target_path.write_bytes(content)
            storage_path = normalize_storage_path(target_path)
            logger.info(
                "File stored at internal path {storage_path}",
                storage_path=storage_path,
            )
            return storage_path
        except OSError as exc:
            logger.exception(
                "Storage error while saving {filename}",
                filename=stored_filename,
            )
            raise StorageProviderError("Storage failure") from exc

    def delete(self, *, storage_path: str) -> None:
        """Delete a stored file if it exists."""
        try:
            path = self._resolve_storage_path(storage_path)
            if path.exists():
                path.unlink()
        except OSError as exc:
            logger.exception(
                "Storage error while deleting {storage_path}",
                storage_path=storage_path,
            )
            raise StorageProviderError("Storage failure") from exc

    def exists(self, *, storage_path: str) -> bool:
        """Return whether a stored file exists."""
        return self._resolve_storage_path(storage_path).is_file()

    def read(self, *, storage_path: str) -> bytes:
        """Read a stored file."""
        try:
            return self._resolve_storage_path(storage_path).read_bytes()
        except OSError as exc:
            logger.exception(
                "Storage error while reading {storage_path}",
                storage_path=storage_path,
            )
            raise StorageProviderError("Storage failure") from exc

    def get_metadata(self, *, storage_path: str) -> StoredFileMetadata:
        """Return filesystem metadata for a stored file."""
        try:
            path = self._resolve_storage_path(storage_path)
            stat_result = path.stat()
            return StoredFileMetadata(
                storage_path=normalize_storage_path(path),
                size=stat_result.st_size,
                modified_time=datetime.fromtimestamp(stat_result.st_mtime, UTC),
            )
        except OSError as exc:
            logger.exception(
                "Storage error while reading metadata {storage_path}",
                storage_path=storage_path,
            )
            raise StorageProviderError("Storage failure") from exc

    def _resolve_storage_path(self, storage_path: str) -> Path:
        """Resolve a stored path and prevent traversal outside storage root."""
        path = Path(storage_path)
        resolved_path = path.resolve()
        resolved_base = self._base_path.resolve()
        is_inside_storage = resolved_base in resolved_path.parents
        if not is_inside_storage and resolved_path != resolved_base:
            raise StorageProviderError("Storage failure")
        return resolved_path
