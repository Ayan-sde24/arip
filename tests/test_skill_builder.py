"""Unit tests for the Skill Builder."""

from datetime import UTC, datetime
from uuid import uuid4

import pytest

from app.application.document_analysis.cir_statistics import CIRStatistics
from app.application.resume_builder.skill_builder import SkillBuilder
from app.application.resume_builder.skill_validator import (
    SkillValidationError,
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


def _setup_cir_with_skills_content(
    skill_text: str,
) -> CanonicalIntermediateRepresentation:
    """Helper to mock a CIR containing a Skills section with specified text."""
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
            TextBlock(text=skill_text, page=1, block_index=0, reading_order=0)
        ],
    )

    content = DocumentContent(
        document=document,
        pages=[page],
        raw_text=skill_text,
        clean_text=skill_text,
    )

    section = DocumentSection(
        id=uuid4(),
        section_type=SectionType.SKILLS,
        title="Skills",
        content=skill_text,
        page_number=1,
        start_block=0,
        end_block=0,
        confidence=1.0,
    )

    stats = CIRStatistics(
        total_pages=1,
        total_sections=1,
        total_text_blocks=1,
        total_characters=len(skill_text),
        total_words=len(skill_text.split()),
        detected_languages=["en"],
        average_section_length=len(skill_text),
    )

    return CanonicalIntermediateRepresentation(
        document=document,
        document_content=content,
        sections=[section],
        statistics=stats,
        pipeline_version="1.0",
    )


def test_build_skills_with_categories() -> None:
    """Test parsing skills structured with category headers."""
    skill_text = "Languages: Python, Go, JavaScript\n" "Frameworks: FastAPI, React"
    cir = _setup_cir_with_skills_content(skill_text)

    builder = SkillBuilder()
    skills = builder.build(cir=cir)

    assert len(skills) == 5
    assert skills[0].name == "Python"
    assert skills[0].category == "Languages"
    assert skills[3].name == "FastAPI"
    assert skills[3].category == "Frameworks"


def test_build_skills_with_proficiencies() -> None:
    """Test parsing skills containing parenthesized proficiency markers."""
    skill_text = "Python (Advanced), Go (Intermediate), SQL"
    cir = _setup_cir_with_skills_content(skill_text)

    builder = SkillBuilder()
    skills = builder.build(cir=cir)

    assert len(skills) == 3
    assert skills[0].name == "Python"
    assert skills[0].proficiency == "Advanced"
    assert skills[1].name == "Go"
    assert skills[1].proficiency == "Intermediate"
    assert skills[2].name == "SQL"
    assert skills[2].proficiency is None


def test_build_missing_skill_name() -> None:
    """Test validation fails when skill name is missing."""
    from app.application.resume_builder.skill_validator import (
        SkillValidator,
    )

    validator = SkillValidator()
    errors = validator.validate(
        [
            {
                "name": "",
                "category": "Languages",
            }
        ]
    )
    assert "record_0.name" in errors


def test_build_duplicate_skills() -> None:
    """Test validation fails when duplicate skill names are detected."""
    from app.application.resume_builder.skill_validator import (
        SkillValidator,
    )

    validator = SkillValidator()
    errors = validator.validate(
        [
            {
                "name": "Python",
            },
            {
                "name": "Python",
            },
        ]
    )
    assert "record_1.duplicate" in errors


def test_build_empty_skills_section() -> None:
    """Test validation fails when skills section is empty."""
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

    builder = SkillBuilder()
    with pytest.raises(SkillValidationError, match="Skills section cannot be empty"):
        builder.build(cir=cir)
