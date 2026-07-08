"""Unit tests for the Certification Builder."""

from datetime import UTC, datetime
from uuid import uuid4

import pytest

from app.application.document_analysis.cir_statistics import CIRStatistics
from app.application.resume_builder.certification_builder import (
    CertificationBuilder,
)
from app.application.resume_builder.certification_validator import (
    CertificationValidationError,
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


def _setup_cir_with_certifications_content(
    cert_text: str,
) -> CanonicalIntermediateRepresentation:
    """Helper to mock a CIR containing a Certifications section with specified text."""
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
        text_blocks=[TextBlock(text=cert_text, page=1, block_index=0, reading_order=0)],
    )

    content = DocumentContent(
        document=document,
        pages=[page],
        raw_text=cert_text,
        clean_text=cert_text,
    )

    section = DocumentSection(
        id=uuid4(),
        section_type=SectionType.CERTIFICATIONS,
        title="Certifications",
        content=cert_text,
        page_number=1,
        start_block=0,
        end_block=0,
        confidence=1.0,
    )

    stats = CIRStatistics(
        total_pages=1,
        total_sections=1,
        total_text_blocks=1,
        total_characters=len(cert_text),
        total_words=len(cert_text.split()),
        detected_languages=["en"],
        average_section_length=len(cert_text),
    )

    return CanonicalIntermediateRepresentation(
        document=document,
        document_content=content,
        sections=[section],
        statistics=stats,
        pipeline_version="1.0",
    )


def test_build_single_certification() -> None:
    """Test parsing a single valid certification entry successfully."""
    cert_text = "AWS Certified Solutions Architect - Amazon Web Services | 2021 - 2024 (https://cred.ly/123)"
    cir = _setup_cir_with_certifications_content(cert_text)

    builder = CertificationBuilder()
    certifications = builder.build(cir=cir)

    assert len(certifications) == 1
    cert = certifications[0]
    assert cert.name == "AWS Certified Solutions Architect"
    assert cert.issuer == "Amazon Web Services"
    assert cert.issue_date == "2021"
    assert cert.expiration_date == "2024"
    assert cert.url == "https://cred.ly/123"


def test_build_multiple_certifications() -> None:
    """Test parsing multiple valid certification entries successfully."""
    cert_text = (
        "AWS Certified Solutions Architect - Amazon Web Services | 2021\n"
        "Certified Scrum Master - Scrum Alliance | 2020"
    )
    cir = _setup_cir_with_certifications_content(cert_text)

    builder = CertificationBuilder()
    certifications = builder.build(cir=cir)

    assert len(certifications) == 2
    assert certifications[0].name == "AWS Certified Solutions Architect"
    assert certifications[0].issuer == "Amazon Web Services"
    assert certifications[0].issue_date == "2021"

    assert certifications[1].name == "Certified Scrum Master"
    assert certifications[1].issuer == "Scrum Alliance"
    assert certifications[1].issue_date == "2020"


def test_build_missing_certification_name() -> None:
    """Test validation fails when certification name is missing."""
    from app.application.resume_builder.certification_validator import (
        CertificationValidator,
    )

    validator = CertificationValidator()
    errors = validator.validate(
        [
            {
                "name": "",
                "issuer": "Scrum Alliance",
            }
        ]
    )
    assert "record_0.name" in errors


def test_build_duplicate_certifications() -> None:
    """Test validation fails when duplicate certifications are detected."""
    from app.application.resume_builder.certification_validator import (
        CertificationValidator,
    )

    validator = CertificationValidator()
    errors = validator.validate(
        [
            {
                "name": "AWS Solutions Architect",
                "issuer": "AWS",
            },
            {
                "name": "AWS Solutions Architect",
                "issuer": "AWS",
            },
        ]
    )
    assert "record_1.duplicate" in errors


def test_build_invalid_dates() -> None:
    """Test validation fails when start/issue year is after expiration year."""
    from app.application.resume_builder.certification_validator import (
        CertificationValidator,
    )

    validator = CertificationValidator()
    errors = validator.validate(
        [
            {
                "name": "AWS Solutions Architect",
                "issue_date": "2024",
                "expiration_date": "2021",
            }
        ]
    )
    assert "record_0.dates" in errors


def test_build_empty_certifications_section() -> None:
    """Test validation fails when certifications section is empty."""
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
    content = DocumentContent(
        document=document,
        pages=[Page(page_number=1, text_blocks=[])],
    )
    stats = CIRStatistics(
        total_pages=1,
        total_sections=0,
        total_text_blocks=0,
        total_characters=0,
        total_words=0,
        detected_languages=[],
        average_section_length=0.0,
    )
    cir = CanonicalIntermediateRepresentation(
        document=document,
        document_content=content,
        sections=[],
        statistics=stats,
    )

    builder = CertificationBuilder()
    with pytest.raises(
        CertificationValidationError,
        match="Certifications section cannot be empty",
    ):
        builder.build(cir=cir)
