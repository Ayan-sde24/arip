"""Domain entity representing a structured document with classified sections."""

from dataclasses import dataclass, field
from typing import Any

from app.domain.entities.document import Document
from app.domain.entities.document_content import DocumentContent
from app.domain.entities.document_section import DocumentSection
from app.domain.entities.section_type import SectionType


@dataclass(frozen=True)
class StructuredDocument:
    """Immutable domain entity representing a structured document.

    Attributes:
        document: The source document or document content containing file
            details.
        sections: List of logical sections parsed/detected from the document.
        statistics: Qualitative/quantitative metrics about the structured document.
        metadata: Arbitrary metadata associated with the structure.
    """

    document: Document | DocumentContent
    sections: list[DocumentSection] = field(default_factory=list)
    statistics: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def get_section(self, section_type: SectionType) -> DocumentSection | None:
        """Retrieve the first section matching the given section type.

        Args:
            section_type: The type of section to find.

        Returns:
            The first matching DocumentSection, or None if not found.
        """
        for section in self.sections:
            if section.section_type == section_type:
                return section
        return None

    def find_sections(self, section_type: SectionType) -> list[DocumentSection]:
        """Find all sections matching the given section type.

        Args:
            section_type: The type of sections to find.

        Returns:
            A list of matching DocumentSection entities.
        """
        return [
            section for section in self.sections if section.section_type == section_type
        ]

    def has_section(self, section_type: SectionType) -> bool:
        """Check if the document contains at least one section of the given type.

        Args:
            section_type: The type of section to check for.

        Returns:
            True if a matching section exists, False otherwise.
        """
        return any(section.section_type == section_type for section in self.sections)
