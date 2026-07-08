"""Domain entity representing a logical section within a document."""

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID

from app.domain.entities.section_type import SectionType


@dataclass(frozen=True)
class DocumentSection:
    """Immutable domain entity representing a logical section in a document.

    Attributes:
        id: Unique identifier for the section.
        section_type: The classified category of this section.
        title: The heading or title of the section, or None if unheaded.
        content: The text content of the section.
        page_number: 1-based page number where the section starts.
        start_block: 0-based block index where the section starts.
        end_block: 0-based block index where the section ends.
        confidence: Classification confidence score between 0.0 and 1.0.
        metadata: Additional arbitrary metadata associated with the section.
    """

    id: UUID
    section_type: SectionType
    title: str | None
    content: str
    page_number: int
    start_block: int
    end_block: int
    confidence: float
    metadata: dict[str, Any] = field(default_factory=dict)
