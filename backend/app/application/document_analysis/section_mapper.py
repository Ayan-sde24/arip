"""Heading normalization and mapping service to build DocumentSection."""

from uuid import uuid4

from app.application.document_analysis.section_boundary import SectionBoundary
from app.domain.entities.document_content import DocumentContent
from app.domain.entities.document_section import DocumentSection
from app.domain.entities.section_type import SectionType


class SectionMapper:
    """Mapper class that maps section headings to DocumentSection entities."""

    # Normalization mapping based on keywords
    MAPPING_RULES = [
        # (list of matching keywords, SectionType)
        (
            ["education", "academic", "university", "school", "degree"],
            SectionType.EDUCATION,
        ),
        (
            [
                "experience",
                "work",
                "employment",
                "career",
                "history",
                "professional",
            ],
            SectionType.EXPERIENCE,
        ),
        (["project", "portfolio"], SectionType.PROJECTS),
        (
            ["skill", "competenc", "technolog", "expertise", "tool"],
            SectionType.SKILLS,
        ),
        (["certif", "licens", "credential"], SectionType.CERTIFICATIONS),
        (["achievement", "accomplishment"], SectionType.ACHIEVEMENTS),
        (["award", "honor"], SectionType.AWARDS),
        (["language"], SectionType.LANGUAGES),
        (["publication", "paper", "research", "patent"], SectionType.PUBLICATIONS),
        (["volunteer"], SectionType.VOLUNTEER),
        (["interest", "hobby", "hobbies"], SectionType.INTERESTS),
        (["profile", "about"], SectionType.PROFILE),
        (["summary", "objective", "overview"], SectionType.SUMMARY),
        (["contact", "info", "address", "email", "phone"], SectionType.CONTACT),
    ]

    def map_boundary_to_section(
        self,
        *,
        content: DocumentContent,
        boundary: SectionBoundary,
    ) -> DocumentSection:
        """Map a SectionBoundary to a resolved DocumentSection domain entity.

        Args:
            content: The DocumentContent source.
            boundary: The SectionBoundary coordinates.

        Returns:
            A constructed DocumentSection entity.
        """
        # 1. Extract content from boundary blocks
        extracted_text = self._extract_content(content, boundary)

        # 2. Determine SectionType
        title = boundary.heading.text if boundary.heading else None
        section_type = self.determine_section_type(title)

        # 3. Build DocumentSection
        heading_confidence = boundary.heading.confidence if boundary.heading else 1.0
        return DocumentSection(
            id=uuid4(),
            section_type=section_type,
            title=title,
            content=extracted_text,
            page_number=boundary.start_page,
            start_block=boundary.start_block,
            end_block=boundary.end_block,
            confidence=boundary.confidence,
            metadata={
                "boundary_id": str(boundary.boundary_id),
                "heading_confidence": heading_confidence,
            },
        )

    def determine_section_type(self, title: str | None) -> SectionType:
        """Normalize the heading title and match it to a SectionType.

        Args:
            title: The raw heading title, or None.

        Returns:
            The mapped SectionType.
        """
        if title is None:
            # Leading content defaults to CONTACT or OTHER
            return SectionType.CONTACT

        normalized = title.lower().strip().replace(":", "").replace("-", " ")
        words = normalized.split()

        for keywords, sec_type in self.MAPPING_RULES:
            for word in words:
                for kw in keywords:
                    # Match if word contains or is equal to the keyword
                    if kw in word:
                        return sec_type

        return SectionType.OTHER

    def _extract_content(
        self,
        content: DocumentContent,
        boundary: SectionBoundary,
    ) -> str:
        """Collect and concatenate all TextBlock text within the boundary range."""
        blocks: list[str] = []

        for p_idx in range(boundary.start_page, boundary.end_page + 1):
            if p_idx > len(content.pages):
                break
            page = content.pages[p_idx - 1]

            start_b = boundary.start_block if p_idx == boundary.start_page else 0
            end_b = (
                boundary.end_block
                if p_idx == boundary.end_page
                else len(page.text_blocks) - 1
            )

            for b_idx in range(start_b, end_b + 1):
                if b_idx < len(page.text_blocks):
                    blocks.append(page.text_blocks[b_idx].text)

        return "\n".join(blocks)
