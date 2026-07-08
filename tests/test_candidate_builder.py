"""Unit tests for the Candidate Builder (TICKET-006.1)."""

from datetime import UTC, datetime
from uuid import uuid4

import pytest

from app.application.document_analysis.cir_statistics import CIRStatistics
from app.application.resume_builder.candidate_builder import CandidateBuilder
from app.application.resume_builder.candidate_validator import (
    CandidateValidationError,
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


def _setup_cir_with_contact_content(
    contact_text: str,
) -> CanonicalIntermediateRepresentation:
    """Helper to mock a CIR containing a Contact section with specified text."""
    doc_id = uuid4()
    now = datetime.now(UTC)

    document = Document(
        document_id=doc_id,
        document_type=DocumentType.RESUME,
        original_filename="cv.pdf",
        stored_filename=f"{doc_id}.pdf",
        mime_type="application/pdf",
        extension="pdf",
        checksum="12345abc",
        size=1024,
        created_at=now,
        updated_at=now,
        status=DocumentStatus.UPLOADED,
    )

    page = Page(
        page_number=1,
        text_blocks=[
            TextBlock(text=contact_text, page=1, block_index=0, reading_order=0)
        ],
    )

    content = DocumentContent(
        document=document,
        pages=[page],
        raw_text=contact_text,
        clean_text=contact_text,
    )

    section = DocumentSection(
        id=uuid4(),
        section_type=SectionType.CONTACT,
        title="Contact Info",
        content=contact_text,
        page_number=1,
        start_block=0,
        end_block=0,
        confidence=1.0,
    )

    stats = CIRStatistics(
        total_pages=1,
        total_sections=1,
        total_text_blocks=1,
        total_characters=len(contact_text),
        total_words=len(contact_text.split()),
        detected_languages=["en"],
        average_section_length=len(contact_text),
    )

    return CanonicalIntermediateRepresentation(
        document=document,
        document_content=content,
        sections=[section],
        statistics=stats,
        pipeline_version="1.0",
    )


def test_build_valid_candidate() -> None:
    """Test building a candidate with all valid properties successfully."""
    contact_text = (
        "Alice Smith\n"
        "alice.smith@example.com\n"
        "+1 (555) 019-2834\n"
        "San Francisco, CA\n"
        "https://linkedin.com/in/alicesmith\n"
        "https://github.com/alicesmith\n"
        "https://alicesmith.dev"
    )
    cir = _setup_cir_with_contact_content(contact_text)

    builder = CandidateBuilder()
    candidate = builder.build(cir=cir)

    assert candidate.name == "Alice Smith"
    assert candidate.email == "alice.smith@example.com"
    assert candidate.phone == "+1 (555) 019-2834"
    assert candidate.location == "San Francisco, CA"
    assert candidate.linkedin == "https://linkedin.com/in/alicesmith"
    assert candidate.github == "https://github.com/alicesmith"
    assert candidate.portfolio == "https://alicesmith.dev"


def test_build_missing_name() -> None:
    """Test validation fails when candidate name is missing/unextractable."""
    # Contact block only has email and phone
    contact_text = "alice.smith@example.com\n+1 (555) 019-2834"
    cir = _setup_cir_with_contact_content(contact_text)

    builder = CandidateBuilder()
    with pytest.raises(CandidateValidationError, match="Name is required"):
        builder.build(cir=cir)


def test_build_missing_email() -> None:
    """Test validation fails when email is missing."""
    contact_text = "Alice Smith\n+1 (555) 019-2834"
    cir = _setup_cir_with_contact_content(contact_text)

    builder = CandidateBuilder()
    with pytest.raises(CandidateValidationError, match="Email is required"):
        builder.build(cir=cir)


def test_build_missing_phone() -> None:
    """Test validation fails when phone number is missing."""
    contact_text = "Alice Smith\nalice@example.com"
    cir = _setup_cir_with_contact_content(contact_text)

    builder = CandidateBuilder()
    with pytest.raises(CandidateValidationError, match="Phone is required"):
        builder.build(cir=cir)


def test_build_duplicate_email() -> None:
    """Test validation fails when duplicate/multiple email patterns are extracted."""
    contact_text = "Alice Smith\nalice@example.com alice@example.com\n+1 (555) 019-2834"
    cir = _setup_cir_with_contact_content(contact_text)

    builder = CandidateBuilder()
    with pytest.raises(
        CandidateValidationError, match="Duplicate email addresses detected"
    ):
        builder.build(cir=cir)


def test_build_invalid_phone() -> None:
    """Test validation fails when phone number fails format constraint."""
    from app.application.resume_builder.candidate_validator import (
        CandidateValidator,
    )

    validator = CandidateValidator()
    errors = validator.validate(
        {
            "name": "Alice Smith",
            "email": "alice@example.com",
            "phone": "123-abc-456",
        }
    )
    assert "phone" in errors
    assert "Invalid phone format" in errors["phone"]


def test_build_invalid_url() -> None:
    """Test validation fails when URL field fails format constraint."""
    from app.application.resume_builder.candidate_validator import (
        CandidateValidator,
    )

    validator = CandidateValidator()
    errors = validator.validate(
        {
            "name": "Alice Smith",
            "email": "alice@example.com",
            "phone": "+1 (555) 019-2834",
            "linkedin": "not-a-valid-url",
        }
    )
    assert "linkedin" in errors
    assert "Invalid URL format for linkedin" in errors["linkedin"]
