"""Unit tests for the CIR Builder (TICKET-005.5)."""

from datetime import UTC, datetime
from uuid import UUID, uuid4

import pytest

from app.application.document_analysis.cir_builder import (
    CIRBuilder,
    CIRValidationError,
)
from app.domain.entities.canonical_intermediate_representation import (
    CanonicalIntermediateRepresentation,
)
from app.domain.entities.document import Document, DocumentStatus, DocumentType
from app.domain.entities.document_content import DocumentContent
from app.domain.entities.document_section import DocumentSection
from app.domain.entities.page import Page
from app.domain.entities.section_type import SectionType
from app.domain.entities.text_block import TextBlock


def _setup_test_models(
    doc_id: UUID | None = None,
) -> tuple[Document, DocumentContent, list[DocumentSection]]:
    """Helper to create minimal valid inputs for the builder."""
    d_id = doc_id or uuid4()
    now = datetime.now(UTC)

    document = Document(
        document_id=d_id,
        document_type=DocumentType.RESUME,
        original_filename="resume.pdf",
        stored_filename=f"{d_id}.pdf",
        mime_type="application/pdf",
        extension="pdf",
        checksum="12345abcde",
        size=2048,
        created_at=now,
        updated_at=now,
        status=DocumentStatus.UPLOADED,
    )

    blocks_p1 = [
        TextBlock(text="Education", page=1, block_index=0, reading_order=0),
        TextBlock(
            text="University of California",
            page=1,
            block_index=1,
            reading_order=1,
        ),
    ]
    page_1 = Page(page_number=1, text_blocks=blocks_p1)

    document_content = DocumentContent(
        document=document,
        pages=[page_1],
        raw_text="Education\nUniversity of California",
        clean_text="Education University of California",
        language="en",
    )

    section = DocumentSection(
        id=uuid4(),
        section_type=SectionType.EDUCATION,
        title="Education",
        content="Education\nUniversity of California",
        page_number=1,
        start_block=0,
        end_block=1,
        confidence=1.0,
    )

    return document, document_content, [section]


def test_build_cir_success() -> None:
    """Test standard build flow with correct input components."""
    doc, content, sections = _setup_test_models()

    builder = CIRBuilder(pipeline_version="2.1")
    cir = builder.build(
        document=doc,
        document_content=content,
        sections=sections,
        metadata={"custom_flag": "test"},
    )

    assert isinstance(cir, CanonicalIntermediateRepresentation)
    assert cir.document == doc
    assert cir.document_content == content
    assert cir.sections == sections
    assert cir.pipeline_version == "2.1"
    assert cir.metadata["custom_flag"] == "test"
    assert cir.metadata["built_by"] == "CIRBuilder"
    assert cir.created_at is not None


def test_cir_statistics() -> None:
    """Test that statistics are populated accurately from content and sections."""
    doc, content, sections = _setup_test_models()

    builder = CIRBuilder()
    cir = builder.build(
        document=doc,
        document_content=content,
        sections=sections,
    )

    stats = cir.statistics
    assert stats.total_pages == 1
    assert stats.total_sections == 1
    assert stats.total_text_blocks == 2
    assert stats.total_characters == len("Education") + len("University of California")
    assert stats.total_words == 4  # "Education", "University", "of", "California"
    assert stats.detected_languages == ["en"]
    # "Education\nUniversity of California" has 34 characters
    assert stats.average_section_length == 34.0


def test_validation_errors() -> None:
    """Test validation cases that reject invalid build components."""
    doc, content, sections = _setup_test_models()
    builder = CIRBuilder()

    # 1. Reject null document
    with pytest.raises(CIRValidationError, match="Document cannot be null"):
        builder.build(
            document=None,  # type: ignore[arg-type]
            document_content=content,
            sections=sections,
        )

    # 2. Reject null document content
    with pytest.raises(CIRValidationError, match="Document content cannot be null"):
        builder.build(
            document=doc,
            document_content=None,  # type: ignore[arg-type]
            sections=sections,
        )

    # 3. Reject empty section list
    with pytest.raises(CIRValidationError, match="Section list cannot be empty"):
        builder.build(
            document=doc,
            document_content=content,
            sections=[],
        )

    # 4. Reject document ID mismatch
    wrong_doc_id = uuid4()
    wrong_doc, _, _ = _setup_test_models(doc_id=wrong_doc_id)
    with pytest.raises(
        CIRValidationError,
        match="DocumentContent document ID does not match Document ID",
    ):
        builder.build(
            document=wrong_doc,
            document_content=content,
            sections=sections,
        )

    # 5. Reject duplicate section IDs
    dup_section = DocumentSection(
        id=sections[0].id,  # Duplicate ID
        section_type=SectionType.EXPERIENCE,
        title="Experience",
        content="Developer role.",
        page_number=1,
        start_block=0,
        end_block=0,
        confidence=0.9,
    )
    with pytest.raises(CIRValidationError, match="Duplicate section ID detected"):
        builder.build(
            document=doc,
            document_content=content,
            sections=[sections[0], dup_section],
        )
