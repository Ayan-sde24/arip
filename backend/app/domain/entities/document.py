"""Domain entities representing document concepts in the system."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from typing import Any
from uuid import UUID


class DocumentStatus(StrEnum):
    """Business status of a document as it moves through the processing lifecycle."""

    UPLOADED = "uploaded"
    VALIDATED = "validated"
    STORED = "stored"
    PROCESSING = "processing"
    PARSED = "parsed"
    ANALYZED = "analyzed"
    FAILED = "failed"
    ARCHIVED = "archived"


class DocumentType(StrEnum):
    """Logical categories of documents supported by the platform."""

    RESUME = "resume"
    JOB_DESCRIPTION = "job_description"
    COVER_LETTER = "cover_letter"
    CERTIFICATE = "certificate"
    TRANSCRIPT = "transcript"
    PORTFOLIO = "portfolio"
    RESEARCH_PAPER = "research_paper"
    REPORT = "report"


@dataclass(frozen=True)
class Document:
    """Core domain business entity representing an uploaded and managed document."""

    document_id: UUID
    document_type: DocumentType
    original_filename: str
    stored_filename: str
    mime_type: str
    extension: str
    checksum: str
    size: int
    created_at: datetime
    updated_at: datetime
    status: DocumentStatus
    metadata: dict[str, Any] = field(default_factory=dict)
