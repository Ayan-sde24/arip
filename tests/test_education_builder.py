"""Unit tests for the Education Builder (TICKET-006.2)."""

from datetime import UTC, datetime
from uuid import uuid4

import pytest

from app.application.document_analysis.cir_statistics import CIRStatistics
from app.application.resume_builder.education_builder import EducationBuilder
from app.application.resume_builder.education_validator import (
    EducationValidationError,
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


def _setup_cir_with_education_content(
    edu_text: str,
) -> CanonicalIntermediateRepresentation:
    """Helper to mock a CIR containing an Education section with specified text."""
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
        text_blocks=[TextBlock(text=edu_text, page=1, block_index=0, reading_order=0)],
    )

    content = DocumentContent(
        document=document,
        pages=[page],
        raw_text=edu_text,
        clean_text=edu_text,
    )

    section = DocumentSection(
        id=uuid4(),
        section_type=SectionType.EDUCATION,
        title="Education",
        content=edu_text,
        page_number=1,
        start_block=0,
        end_block=0,
        confidence=1.0,
    )

    stats = CIRStatistics(
        total_pages=1,
        total_sections=1,
        total_text_blocks=1,
        total_characters=len(edu_text),
        total_words=len(edu_text.split()),
        detected_languages=["en"],
        average_section_length=len(edu_text),
    )

    return CanonicalIntermediateRepresentation(
        document=document,
        document_content=content,
        sections=[section],
        statistics=stats,
        pipeline_version="1.0",
    )


def test_build_single_education() -> None:
    """Test parsing a single valid education entry successfully."""
    edu_text = (
        "Stanford University\n"
        "Bachelor of Science in Computer Science\n"
        "Sep 2018 - Jun 2022\n"
        "GPA: 3.95\n"
        "Minored in Economics"
    )
    cir = _setup_cir_with_education_content(edu_text)

    builder = EducationBuilder()
    education_list = builder.build(cir=cir)

    assert len(education_list) == 1
    edu = education_list[0]
    assert edu.institution == "Stanford University"
    assert edu.degree == "Bachelor of Science"
    assert edu.major == "Computer Science"
    assert edu.start_date == "Sep 2018"
    assert edu.end_date == "Jun 2022"
    assert edu.gpa == 3.95
    assert edu.details == ["Minored in Economics"]


def test_build_multiple_education_entries() -> None:
    """Test parsing multiple valid education entries successfully."""
    edu_text = (
        "Harvard University\n"
        "Master of Science in Software Engineering\n"
        "2022 - 2024\n"
        "GPA: 4.0\n"
        "Stanford University\n"
        "Bachelor of Science in Computer Science\n"
        "2018 - 2022"
    )
    cir = _setup_cir_with_education_content(edu_text)

    builder = EducationBuilder()
    education_list = builder.build(cir=cir)

    assert len(education_list) == 2
    assert education_list[0].institution == "Harvard University"
    assert education_list[0].degree == "Master of Science"
    assert education_list[0].major == "Software Engineering"
    assert education_list[0].start_date == "2022"
    assert education_list[0].end_date == "2024"
    assert education_list[0].gpa == 4.0

    assert education_list[1].institution == "Stanford University"
    assert education_list[1].degree == "Bachelor of Science"
    assert education_list[1].major == "Computer Science"
    assert education_list[1].start_date == "2018"
    assert education_list[1].end_date == "2022"


def test_build_missing_institution() -> None:
    """Test validation fails when institution field is missing."""
    # Instantiate input records directly to test required constraint
    from app.application.resume_builder.education_validator import (
        EducationValidator,
    )

    validator = EducationValidator()
    errors = validator.validate(
        [
            {
                "institution": "",
                "degree": "Bachelor of Science",
                "major": "Computer Science",
            }
        ]
    )
    assert "record_0.institution" in errors


def test_build_missing_degree() -> None:
    """Test validation fails when degree field is missing."""
    from app.application.resume_builder.education_validator import (
        EducationValidator,
    )

    validator = EducationValidator()
    errors = validator.validate(
        [
            {
                "institution": "Stanford University",
                "degree": "",
                "major": "Computer Science",
            }
        ]
    )
    assert "record_0.degree" in errors


def test_build_duplicate_education() -> None:
    """Test validation fails when duplicate education entries are detected."""
    from app.application.resume_builder.education_validator import (
        EducationValidator,
    )

    validator = EducationValidator()
    errors = validator.validate(
        [
            {
                "institution": "Stanford University",
                "degree": "Bachelor of Science",
                "major": "Computer Science",
            },
            {
                "institution": "Stanford University",
                "degree": "Bachelor of Science",
                "major": "Computer Science",
            },
        ]
    )
    assert "record_1.duplicate" in errors


def test_build_invalid_dates() -> None:
    """Test validation fails when start date year is after end date year."""
    from app.application.resume_builder.education_validator import (
        EducationValidator,
    )

    validator = EducationValidator()
    errors = validator.validate(
        [
            {
                "institution": "Stanford University",
                "degree": "Bachelor of Science",
                "major": "Computer Science",
                "start_date": "2022",
                "end_date": "2018",
            }
        ]
    )
    assert "record_0.dates" in errors
    assert "cannot be after end year" in errors["record_0.dates"][0]


def test_build_empty_education_section() -> None:
    """Test validation fails when the education section is empty/missing."""
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
    # CIR with empty sections
    cir = CanonicalIntermediateRepresentation(
        document=document,
        document_content=content,
        sections=[],
        statistics=stats,
    )

    builder = EducationBuilder()
    with pytest.raises(
        EducationValidationError, match="Education section cannot be empty"
    ):
        builder.build(cir=cir)
