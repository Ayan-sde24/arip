"""Unit tests for the Achievement Builder."""

from datetime import UTC, datetime
from uuid import uuid4

import pytest

from app.application.document_analysis.cir_statistics import CIRStatistics
from app.application.resume_builder.achievement_builder import AchievementBuilder
from app.application.resume_builder.achievement_validator import (
    AchievementValidationError,
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


def _setup_cir_with_achievements_content(
    ach_text: str,
) -> CanonicalIntermediateRepresentation:
    """Helper to mock a CIR containing an Achievements section with specified text."""
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
        text_blocks=[TextBlock(text=ach_text, page=1, block_index=0, reading_order=0)],
    )

    content = DocumentContent(
        document=document,
        pages=[page],
        raw_text=ach_text,
        clean_text=ach_text,
    )

    section = DocumentSection(
        id=uuid4(),
        section_type=SectionType.ACHIEVEMENTS,
        title="Achievements",
        content=ach_text,
        page_number=1,
        start_block=0,
        end_block=0,
        confidence=1.0,
    )

    stats = CIRStatistics(
        total_pages=1,
        total_sections=1,
        total_text_blocks=1,
        total_characters=len(ach_text),
        total_words=len(ach_text.split()),
        detected_languages=["en"],
        average_section_length=len(ach_text),
    )

    return CanonicalIntermediateRepresentation(
        document=document,
        document_content=content,
        sections=[section],
        statistics=stats,
        pipeline_version="1.0",
    )


def test_build_single_achievement() -> None:
    """Test parsing a single valid achievement successfully."""
    ach_text = "Hackathon Winner - Won first place in 2022 among 100 teams."
    cir = _setup_cir_with_achievements_content(ach_text)

    builder = AchievementBuilder()
    achievements = builder.build(cir=cir)

    assert len(achievements) == 1
    ach = achievements[0]
    assert ach.title == "Hackathon Winner"
    assert "Won first place" in ach.description
    assert ach.date == "2022"


def test_build_multiple_achievements() -> None:
    """Test parsing multiple valid achievements successfully."""
    ach_text = (
        "Hackathon Winner - Won first place | 2022\n"
        "Dean's List - Academic excellence | 2018"
    )
    cir = _setup_cir_with_achievements_content(ach_text)

    builder = AchievementBuilder()
    achievements = builder.build(cir=cir)

    assert len(achievements) == 2
    assert achievements[0].title == "Hackathon Winner"
    assert achievements[0].date == "2022"

    assert achievements[1].title == "Dean's List"
    assert achievements[1].date == "2018"


def test_build_missing_achievement_title() -> None:
    """Test validation fails when achievement title is missing."""
    from app.application.resume_builder.achievement_validator import (
        AchievementValidator,
    )

    validator = AchievementValidator()
    errors = validator.validate(
        [
            {
                "title": "",
                "description": "Scored top marks",
            }
        ]
    )
    assert "record_0.title" in errors


def test_build_missing_achievement_description() -> None:
    """Test validation fails when achievement description is missing."""
    from app.application.resume_builder.achievement_validator import (
        AchievementValidator,
    )

    validator = AchievementValidator()
    errors = validator.validate(
        [
            {
                "title": "Scholarship",
                "description": "",
            }
        ]
    )
    assert "record_0.description" in errors


def test_build_duplicate_achievements() -> None:
    """Test validation fails when duplicate achievements are detected."""
    from app.application.resume_builder.achievement_validator import (
        AchievementValidator,
    )

    validator = AchievementValidator()
    errors = validator.validate(
        [
            {
                "title": "Scholarship",
                "description": "desc 1",
            },
            {
                "title": "Scholarship",
                "description": "desc 2",
            },
        ]
    )
    assert "record_1.duplicate" in errors


def test_build_empty_achievements_section() -> None:
    """Test validation fails when achievements section is empty."""
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

    builder = AchievementBuilder()
    with pytest.raises(
        AchievementValidationError, match="Achievements section cannot be empty"
    ):
        builder.build(cir=cir)
