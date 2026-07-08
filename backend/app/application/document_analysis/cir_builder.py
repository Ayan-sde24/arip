"""Builder class for assembling the Canonical Intermediate Representation (CIR)."""

from datetime import UTC, datetime
from typing import Any

from app.application.document_analysis.cir_statistics import CIRStatistics
from app.domain.entities.canonical_intermediate_representation import (
    CanonicalIntermediateRepresentation,
)
from app.domain.entities.document import Document
from app.domain.entities.document_content import DocumentContent
from app.domain.entities.document_section import DocumentSection


class CIRValidationError(Exception):
    """Exception raised when validation of CIR input components fails."""

    pass


class CIRBuilder:
    """Builder class responsible for validating and constructing a CIR entity."""

    def __init__(self, pipeline_version: str = "1.0") -> None:
        """Initialize the CIR builder.

        Args:
            pipeline_version: Version string for the processing pipeline.
        """
        self.pipeline_version = pipeline_version

    def build(
        self,
        *,
        document: Document,
        document_content: DocumentContent,
        sections: list[DocumentSection],
        metadata: dict[str, Any] | None = None,
    ) -> CanonicalIntermediateRepresentation:
        """Validate inputs and construct a CanonicalIntermediateRepresentation.

        Args:
            document: Source document metadata.
            document_content: Processed document layout and text.
            sections: Detected document sections.
            metadata: Custom metadata dictionary.

        Returns:
            An immutable CanonicalIntermediateRepresentation instance.

        Raises:
            CIRValidationError: If validation checks fail.
        """
        # 1. Validation
        if document is None:
            raise CIRValidationError("Document cannot be null")
        if document_content is None:
            raise CIRValidationError("Document content cannot be null")
        if not sections:
            raise CIRValidationError("Section list cannot be empty")

        # Validate matching document IDs
        if document_content.document.document_id != document.document_id:
            raise CIRValidationError(
                "DocumentContent document ID does not match Document ID"
            )

        # Validate duplicate section IDs
        seen_ids = set()
        for sec in sections:
            if sec.id in seen_ids:
                raise CIRValidationError(f"Duplicate section ID detected: {sec.id}")
            seen_ids.add(sec.id)

        # 2. Compute Statistics
        stats = self._calculate_statistics(document_content, sections)

        # 3. Assemble Metadata
        cir_metadata = metadata.copy() if metadata is not None else {}
        cir_metadata.setdefault("built_by", "CIRBuilder")

        # 4. Construct CIR
        return CanonicalIntermediateRepresentation(
            document=document,
            document_content=document_content,
            sections=sections,
            statistics=stats,
            metadata=cir_metadata,
            created_at=datetime.now(UTC),
            pipeline_version=self.pipeline_version,
        )

    def _calculate_statistics(
        self,
        content: DocumentContent,
        sections: list[DocumentSection],
    ) -> CIRStatistics:
        """Calculate statistics across pages, blocks, and sections."""
        total_pages = len(content.pages)
        total_sections = len(sections)

        total_text_blocks = 0
        total_characters = 0
        total_words = 0

        for page in content.pages:
            total_text_blocks += len(page.text_blocks)
            for block in page.text_blocks:
                total_characters += len(block.text)
                total_words += len(block.text.split())

        detected_languages = [content.language] if content.language else ["unknown"]

        if total_sections > 0:
            # Average section length in characters
            average_section_length = (
                sum(len(sec.content) for sec in sections) / total_sections
            )
        else:
            average_section_length = 0.0

        return CIRStatistics(
            total_pages=total_pages,
            total_sections=total_sections,
            total_text_blocks=total_text_blocks,
            total_characters=total_characters,
            total_words=total_words,
            detected_languages=detected_languages,
            average_section_length=round(average_section_length, 2),
        )
