"""Protocol defining the interface for section detection engines."""

from typing import Protocol

from app.application.document_analysis.section_boundary import SectionBoundary
from app.domain.entities.document_content import DocumentContent
from app.domain.entities.document_section import DocumentSection


class SectionDetectorProtocol(Protocol):
    """Protocol defining the interface for section detection services."""

    def detect_sections(
        self,
        *,
        content: DocumentContent,
        boundaries: list[SectionBoundary],
    ) -> list[DocumentSection]:
        """Convert section boundaries into classified DocumentSection entities.

        Args:
            content: The DocumentContent source.
            boundaries: The SectionBoundary coordinates list.

        Returns:
            A list of classified DocumentSection domain entities.
        """
        ...
