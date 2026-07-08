"""Unit tests for the Experience Builder (TICKET-006.3)."""

from datetime import UTC, datetime
from uuid import uuid4

import pytest

from app.application.document_analysis.cir_statistics import CIRStatistics
from app.application.resume_builder.experience_builder import ExperienceBuilder
from app.application.resume_builder.experience_validator import (
    ExperienceValidationError,
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


def _setup_cir_with_experience_content(
    exp_text: str,
) -> CanonicalIntermediateRepresentation:
    """Helper to mock a CIR containing an Experience section with specified text."""
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
        text_blocks=[TextBlock(text=exp_text, page=1, block_index=0, reading_order=0)],
    )

    content = DocumentContent(
        document=document,
        pages=[page],
        raw_text=exp_text,
        clean_text=exp_text,
    )

    section = DocumentSection(
        id=uuid4(),
        section_type=SectionType.EXPERIENCE,
        title="Work Experience",
        content=exp_text,
        page_number=1,
        start_block=0,
        end_block=0,
        confidence=1.0,
    )

    stats = CIRStatistics(
        total_pages=1,
        total_sections=1,
        total_text_blocks=1,
        total_characters=len(exp_text),
        total_words=len(exp_text.split()),
        detected_languages=["en"],
        average_section_length=len(exp_text),
    )

    return CanonicalIntermediateRepresentation(
        document=document,
        document_content=content,
        sections=[section],
        statistics=stats,
        pipeline_version="1.0",
    )


def test_build_single_experience() -> None:
    """Test parsing a single valid experience entry successfully."""
    exp_text = (
        "Google Inc. - Software Engineer\n"
        "San Francisco, CA\n"
        "2018 - 2022\n"
        "Developed backend systems using Python.\n"
        "Skills: Python, Go, Docker"
    )
    cir = _setup_cir_with_experience_content(exp_text)

    builder = ExperienceBuilder()
    experience_list = builder.build(cir=cir)

    assert len(experience_list) == 1
    exp = experience_list[0]
    assert exp.company == "Google Inc."
    assert exp.role == "Software Engineer"
    assert exp.location == "San Francisco, CA"
    assert exp.start_date == "2018"
    assert exp.end_date == "2022"
    assert exp.description == ["Developed backend systems using Python."]
    assert exp.skills == ["Python", "Go", "Docker"]


def test_build_multiple_experiences() -> None:
    """Test parsing multiple valid experience entries successfully."""
    exp_text = (
        "Meta Platforms | Engineering Manager | 2022 - 2024\n"
        "Managed a team of engineers.\n"
        "Google Inc. | Software Engineer | 2018 - 2022\n"
        "Developed backend systems."
    )
    cir = _setup_cir_with_experience_content(exp_text)

    builder = ExperienceBuilder()
    experience_list = builder.build(cir=cir)

    assert len(experience_list) == 2
    assert experience_list[0].company == "Meta Platforms"
    assert experience_list[0].role == "Engineering Manager"
    assert experience_list[0].start_date == "2022"
    assert experience_list[0].end_date == "2024"

    assert experience_list[1].company == "Google Inc."
    assert experience_list[1].role == "Software Engineer"
    assert experience_list[1].start_date == "2018"
    assert experience_list[1].end_date == "2022"


def test_build_current_employment() -> None:
    """Test parsing an experience entry representing current employment."""
    exp_text = "Google Inc. - Tech Lead\n" "2020 - Present\n" "Leading teams."
    cir = _setup_cir_with_experience_content(exp_text)

    builder = ExperienceBuilder()
    experience_list = builder.build(cir=cir)

    assert len(experience_list) == 1
    exp = experience_list[0]
    assert exp.company == "Google Inc."
    assert exp.role == "Tech Lead"
    assert exp.start_date == "2020"
    assert exp.end_date == "Present"


def test_build_missing_company() -> None:
    """Test validation fails when company field is missing."""
    from app.application.resume_builder.experience_validator import (
        ExperienceValidator,
    )

    validator = ExperienceValidator()
    errors = validator.validate(
        [
            {
                "company": "",
                "role": "Software Engineer",
                "start_date": "2018",
                "end_date": "2022",
                "current_position": False,
            }
        ]
    )
    assert "record_0.company" in errors


def test_build_missing_job_title() -> None:
    """Test validation fails when job title (role) field is missing."""
    from app.application.resume_builder.experience_validator import (
        ExperienceValidator,
    )

    validator = ExperienceValidator()
    errors = validator.validate(
        [
            {
                "company": "Google Inc.",
                "role": "",
                "start_date": "2018",
                "end_date": "2022",
                "current_position": False,
            }
        ]
    )
    assert "record_0.role" in errors


def test_build_duplicate_records() -> None:
    """Test validation fails when duplicate experience entries are detected."""
    from app.application.resume_builder.experience_validator import (
        ExperienceValidator,
    )

    validator = ExperienceValidator()
    errors = validator.validate(
        [
            {
                "company": "Google Inc.",
                "role": "Software Engineer",
                "start_date": "2018",
                "end_date": "2022",
                "current_position": False,
            },
            {
                "company": "Google Inc.",
                "role": "Software Engineer",
                "start_date": "2022",
                "end_date": "2024",
                "current_position": False,
            },
        ]
    )
    assert "record_1.duplicate" in errors


def test_build_invalid_dates() -> None:
    """Test validation fails when start date year is after end date year."""
    from app.application.resume_builder.experience_validator import (
        ExperienceValidator,
    )

    validator = ExperienceValidator()
    errors = validator.validate(
        [
            {
                "company": "Google Inc.",
                "role": "Software Engineer",
                "start_date": "2022",
                "end_date": "2018",
                "current_position": False,
            }
        ]
    )
    assert "record_0.dates" in errors
    assert "cannot be after end year" in errors["record_0.dates"][0]


def test_build_empty_experience_section() -> None:
    """Test validation fails when the experience section is empty/missing."""
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

    builder = ExperienceBuilder()
    with pytest.raises(
        ExperienceValidationError, match="Experience section cannot be empty"
    ):
        builder.build(cir=cir)
