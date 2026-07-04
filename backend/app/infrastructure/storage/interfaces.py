"""Storage abstractions for dependency inversion."""

from pathlib import PurePath
from typing import Protocol

from app.infrastructure.storage.models import (
    DocumentType,
    FileMetadata,
    StoredFileMetadata,
)


class StorageProvider(Protocol):
    """Provider interface for document persistence backends."""

    def save(
        self,
        *,
        document_type: DocumentType,
        stored_filename: str,
        content: bytes,
    ) -> str:
        """Persist document bytes and return an internal storage path."""

    def delete(self, *, storage_path: str) -> None:
        """Delete a stored document."""

    def exists(self, *, storage_path: str) -> bool:
        """Return whether a stored document exists."""

    def read(self, *, storage_path: str) -> bytes:
        """Read a stored document."""

    def get_metadata(self, *, storage_path: str) -> StoredFileMetadata:
        """Return provider-level metadata for a stored document."""


class StorageService(Protocol):
    """Application-facing document storage service interface."""

    def store_resume(
        self,
        *,
        original_filename: str,
        mime_type: str,
        content: bytes,
    ) -> FileMetadata:
        """Validate and store a resume document."""

    def store_job_description(
        self,
        *,
        original_filename: str,
        mime_type: str,
        content: bytes,
    ) -> FileMetadata:
        """Validate and store a job description document."""

    def store_document(
        self,
        *,
        original_filename: str,
        mime_type: str,
        content: bytes,
        document_type: DocumentType,
    ) -> FileMetadata:
        """Validate and store a generic document type."""


class PathResolver(Protocol):
    """Callable protocol for resolving storage paths."""

    def __call__(self, document_type: DocumentType, filename: str) -> PurePath:
        """Resolve a provider-relative storage path."""
