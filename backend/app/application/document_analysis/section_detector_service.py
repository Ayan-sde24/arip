"""Service implementation for section boundary to DocumentSection conversion."""

from app.application.document_analysis.section_boundary import SectionBoundary
from app.application.document_analysis.section_mapper import SectionMapper
from app.domain.entities.document_content import DocumentContent
from app.domain.entities.document_section import DocumentSection


class SectionDetectorService:
    """Service that converts section boundaries into DocumentSection domain entities."""

    def __init__(self, mapper: SectionMapper | None = None) -> None:
        """Initialize the service with a SectionMapper.

        Args:
            mapper: Custom section mapper, defaults to standard SectionMapper.
        """
        self.mapper = mapper if mapper is not None else SectionMapper()

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
        sections: list[DocumentSection] = []

        # Sort boundaries to preserve document order
        sorted_boundaries = sorted(
            boundaries,
            key=lambda b: (b.start_page, b.start_block),
        )

        for boundary in sorted_boundaries:
            section = self.mapper.map_boundary_to_section(
                content=content,
                boundary=boundary,
            )
            sections.append(section)

        return sections
