"""Validator service for the document intelligence pipeline execution stages."""

from app.application.document_analysis.heading_candidate import HeadingCandidate
from app.application.document_analysis.section_boundary import SectionBoundary
from app.domain.entities.canonical_intermediate_representation import (
    CanonicalIntermediateRepresentation,
)
from app.domain.entities.document import Document
from app.domain.entities.document_content import DocumentContent
from app.domain.entities.document_section import DocumentSection


class PipelineValidator:
    """Validator class to inspect results of each stage in the document pipeline."""

    def validate_input(self, document: Document, content_bytes: bytes) -> list[str]:
        """Validate input document and bytes. Returns list of warning messages."""
        warnings: list[str] = []
        if document is None:
            raise ValueError("Input document cannot be null")
        if not content_bytes:
            raise ValueError("Input document content bytes cannot be empty")
        return warnings

    def validate_reader_output(self, content: DocumentContent | None) -> list[str]:
        """Validate DocumentContent output. Returns list of warning messages."""
        warnings: list[str] = []
        if content is None:
            raise ValueError("DocumentContent was not generated")
        if not content.pages:
            warnings.append("DocumentContent contains no pages")
        elif all(not page.text_blocks for page in content.pages):
            warnings.append("DocumentContent pages contain no text blocks")
        return warnings

    def validate_headings(self, headings: list[HeadingCandidate]) -> list[str]:
        """Validate detected headings. Returns list of warning messages."""
        warnings: list[str] = []
        if not headings:
            warnings.append(
                "No headings detected; document will be processed as a single section"
            )
        return warnings

    def validate_boundaries(self, boundaries: list[SectionBoundary]) -> list[str]:
        """Validate section boundaries. Returns list of warning messages."""
        warnings: list[str] = []
        if not boundaries:
            warnings.append("No section boundaries resolved")
        return warnings

    def validate_sections(self, sections: list[DocumentSection]) -> list[str]:
        """Validate classified sections. Returns list of warning messages."""
        warnings: list[str] = []
        if not sections:
            warnings.append("No sections classified")
        return warnings

    def validate_cir(
        self,
        cir: CanonicalIntermediateRepresentation | None,
    ) -> list[str]:
        """Validate final CIR object. Returns list of warning messages."""
        warnings: list[str] = []
        if cir is None:
            raise ValueError(
                "Canonical Intermediate Representation (CIR) was not generated"
            )
        return warnings
