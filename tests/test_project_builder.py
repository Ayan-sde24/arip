"""Unit tests for the Project Builder."""

from datetime import UTC, datetime
from uuid import uuid4

import pytest

from app.application.document_analysis.cir_statistics import CIRStatistics
from app.application.resume_builder.project_builder import ProjectBuilder
from app.application.resume_builder.project_validator import (
    ProjectValidationError,
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


def _setup_cir_with_projects_content(
    proj_text: str,
) -> CanonicalIntermediateRepresentation:
    """Helper to mock a CIR containing a Projects section with specified text."""
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
        text_blocks=[TextBlock(text=proj_text, page=1, block_index=0, reading_order=0)],
    )

    content = DocumentContent(
        document=document,
        pages=[page],
        raw_text=proj_text,
        clean_text=proj_text,
    )

    section = DocumentSection(
        id=uuid4(),
        section_type=SectionType.PROJECTS,
        title="Projects",
        content=proj_text,
        page_number=1,
        start_block=0,
        end_block=0,
        confidence=1.0,
    )

    stats = CIRStatistics(
        total_pages=1,
        total_sections=1,
        total_text_blocks=1,
        total_characters=len(proj_text),
        total_words=len(proj_text.split()),
        detected_languages=["en"],
        average_section_length=len(proj_text),
    )

    return CanonicalIntermediateRepresentation(
        document=document,
        document_content=content,
        sections=[section],
        statistics=stats,
        pipeline_version="1.0",
    )


def test_build_single_project() -> None:
    """Test parsing a single valid project successfully."""
    proj_text = (
        "Personal Website (https://alice.dev)\n"
        "Built a responsive portfolio site in HTML/CSS and JavaScript.\n"
        "Skills: HTML, CSS, JavaScript"
    )
    cir = _setup_cir_with_projects_content(proj_text)

    builder = ProjectBuilder()
    projects = builder.build(cir=cir)

    assert len(projects) == 1
    proj = projects[0]
    assert proj.title == "Personal Website"
    assert "responsive portfolio site" in proj.description
    assert proj.url == "https://alice.dev"
    assert proj.skills == ["HTML", "CSS", "JavaScript"]


def test_build_multiple_projects() -> None:
    """Test parsing multiple valid projects successfully."""
    proj_text = (
        "Personal Website (https://alice.dev)\n"
        "Built a site in HTML/CSS.\n\n"
        "ARIP Project\n"
        "Implemented document intelligence in Python.\n"
        "Skills: Python, FastAPI"
    )
    cir = _setup_cir_with_projects_content(proj_text)

    builder = ProjectBuilder()
    projects = builder.build(cir=cir)

    assert len(projects) == 2
    assert projects[0].title == "Personal Website"
    assert projects[0].url == "https://alice.dev"

    assert projects[1].title == "ARIP Project"
    assert projects[1].skills == ["Python", "FastAPI"]


def test_build_missing_title() -> None:
    """Test validation fails when project title is missing."""
    from app.application.resume_builder.project_validator import (
        ProjectValidator,
    )

    validator = ProjectValidator()
    errors = validator.validate(
        [
            {
                "title": "",
                "description": "Valid description",
                "url": "https://alice.dev",
            }
        ]
    )
    assert "record_0.title" in errors


def test_build_missing_description() -> None:
    """Test validation fails when project description is missing."""
    from app.application.resume_builder.project_validator import (
        ProjectValidator,
    )

    validator = ProjectValidator()
    errors = validator.validate(
        [
            {
                "title": "Valid Project",
                "description": "",
                "url": "https://alice.dev",
            }
        ]
    )
    assert "record_0.description" in errors


def test_build_duplicate_projects() -> None:
    """Test validation fails when duplicate project titles are detected."""
    from app.application.resume_builder.project_validator import (
        ProjectValidator,
    )

    validator = ProjectValidator()
    errors = validator.validate(
        [
            {
                "title": "My Project",
                "description": "Desc 1",
            },
            {
                "title": "My Project",
                "description": "Desc 2",
            },
        ]
    )
    assert "record_1.duplicate" in errors


def test_build_invalid_url() -> None:
    """Test validation fails when project URL is malformed."""
    from app.application.resume_builder.project_validator import (
        ProjectValidator,
    )

    validator = ProjectValidator()
    errors = validator.validate(
        [
            {
                "title": "Valid Project",
                "description": "Valid desc",
                "url": "invalid-url-string",
            }
        ]
    )
    assert "record_0.url" in errors


def test_build_empty_projects_section() -> None:
    """Test validation fails when projects section is empty."""
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

    builder = ProjectBuilder()
    with pytest.raises(
        ProjectValidationError, match="Projects section cannot be empty"
    ):
        builder.build(cir=cir)
