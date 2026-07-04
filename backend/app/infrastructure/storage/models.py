"""Data models used by the document storage module."""

from datetime import UTC, datetime
from enum import StrEnum
from pathlib import PurePath
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class DocumentType(StrEnum):
    """Supported logical document categories."""

    RESUME = "resume"
    JOB_DESCRIPTION = "job_description"
    DOCUMENT = "document"


class FileMetadata(BaseModel):
    """Metadata captured for a stored document."""

    model_config = ConfigDict(frozen=True)

    id: UUID
    original_filename: str
    stored_filename: str
    extension: str
    mime_type: str
    size: int = Field(ge=0)
    sha256: str
    upload_time: datetime = Field(default_factory=lambda: datetime.now(UTC))
    document_type: DocumentType
    storage_path: str


class StoredFileMetadata(BaseModel):
    """Filesystem-level metadata returned by storage providers."""

    model_config = ConfigDict(frozen=True)

    storage_path: str
    size: int = Field(ge=0)
    modified_time: datetime


def normalize_storage_path(path: PurePath) -> str:
    """Return a portable storage path string."""
    return path.as_posix()
