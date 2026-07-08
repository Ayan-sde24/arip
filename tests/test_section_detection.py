"""Unit tests for the Section Detection Engine (TICKET-005.4)."""

from datetime import UTC, datetime
from uuid import uuid4

from app.application.document_analysis.heading_candidate import HeadingCandidate
from app.application.document_analysis.section_boundary import SectionBoundary
from app.application.document_analysis.section_detector_service import (
    SectionDetectorService,
)
from app.domain.entities.document import Document, DocumentStatus, DocumentType
from app.domain.entities.document_content import DocumentContent
from app.domain.entities.page import Page
from app.domain.entities.section_type import SectionType
from app.domain.entities.text_block import TextBlock


def _create_test_document_content(pages: list[Page]) -> DocumentContent:
    """Helper to create DocumentContent with dummy document metadata."""
    doc_id = uuid4()
    now = datetime.now(UTC)
    doc = Document(
        document_id=doc_id,
        document_type=DocumentType.RESUME,
        original_filename="cv.pdf",
        stored_filename=f"{doc_id}.pdf",
        mime_type="application/pdf",
        extension="pdf",
        checksum="abcd12345",
        size=1024,
        created_at=now,
        updated_at=now,
        status=DocumentStatus.UPLOADED,
    )
    return DocumentContent(document=doc, pages=pages)


def test_section_detection_and_classification() -> None:
    """Test mapping and classification of standard section types."""
    blocks = [
        TextBlock(text="Education", page=1, block_index=0, reading_order=0),
        TextBlock(text="BS in CS", page=1, block_index=1, reading_order=1),
        TextBlock(
            text="Professional Experience",
            page=1,
            block_index=2,
            reading_order=2,
        ),
        TextBlock(text="Software Eng", page=1, block_index=3, reading_order=3),
        TextBlock(text="Projects", page=1, block_index=4, reading_order=4),
        TextBlock(text="Built parser", page=1, block_index=5, reading_order=5),
        TextBlock(text="Technical Skills", page=1, block_index=6, reading_order=6),
        TextBlock(text="Python, Rust", page=1, block_index=7, reading_order=7),
    ]
    page = Page(page_number=1, text_blocks=blocks)
    content = _create_test_document_content([page])

    # Boundaries
    bound_edu = SectionBoundary(
        boundary_id=uuid4(),
        heading=HeadingCandidate(
            text="Education",
            normalized_text="education",
            page_number=1,
            block_index=0,
            confidence=1.0,
        ),
        start_page=1,
        start_block=0,
        end_page=1,
        end_block=1,
        confidence=1.0,
    )

    bound_exp = SectionBoundary(
        boundary_id=uuid4(),
        heading=HeadingCandidate(
            text="Professional Experience",
            normalized_text="professional experience",
            page_number=1,
            block_index=2,
            confidence=1.0,
        ),
        start_page=1,
        start_block=2,
        end_page=1,
        end_block=3,
        confidence=1.0,
    )

    bound_proj = SectionBoundary(
        boundary_id=uuid4(),
        heading=HeadingCandidate(
            text="Projects",
            normalized_text="projects",
            page_number=1,
            block_index=4,
            confidence=1.0,
        ),
        start_page=1,
        start_block=4,
        end_page=1,
        end_block=5,
        confidence=1.0,
    )

    bound_skills = SectionBoundary(
        boundary_id=uuid4(),
        heading=HeadingCandidate(
            text="Technical Skills",
            normalized_text="technical skills",
            page_number=1,
            block_index=6,
            confidence=1.0,
        ),
        start_page=1,
        start_block=6,
        end_page=1,
        end_block=7,
        confidence=1.0,
    )

    detector = SectionDetectorService()
    sections = detector.detect_sections(
        content=content,
        boundaries=[bound_proj, bound_skills, bound_edu, bound_exp],
    )

    # 4 sections, sorted and classified
    assert len(sections) == 4

    # 1. Education
    assert sections[0].section_type == SectionType.EDUCATION
    assert sections[0].title == "Education"
    assert sections[0].content == "Education\nBS in CS"

    # 2. Experience
    assert sections[1].section_type == SectionType.EXPERIENCE
    assert sections[1].title == "Professional Experience"
    assert sections[1].content == "Professional Experience\nSoftware Eng"

    # 3. Projects
    assert sections[2].section_type == SectionType.PROJECTS
    assert sections[2].title == "Projects"
    assert sections[2].content == "Projects\nBuilt parser"

    # 4. Skills
    assert sections[3].section_type == SectionType.SKILLS
    assert sections[3].title == "Technical Skills"
    assert sections[3].content == "Technical Skills\nPython, Rust"


def test_unknown_heading_classification() -> None:
    """Test that unknown headings fallback to OTHER type."""
    blocks = [
        TextBlock(text="Custom Section Title", page=1, block_index=0, reading_order=0),
        TextBlock(text="Custom text.", page=1, block_index=1, reading_order=1),
    ]
    page = Page(page_number=1, text_blocks=blocks)
    content = _create_test_document_content([page])

    boundary = SectionBoundary(
        boundary_id=uuid4(),
        heading=HeadingCandidate(
            text="Custom Section Title",
            normalized_text="custom section title",
            page_number=1,
            block_index=0,
            confidence=0.8,
        ),
        start_page=1,
        start_block=0,
        end_page=1,
        end_block=1,
        confidence=1.0,
    )

    detector = SectionDetectorService()
    sections = detector.detect_sections(content=content, boundaries=[boundary])

    assert len(sections) == 1
    assert sections[0].section_type == SectionType.OTHER
    assert sections[0].title == "Custom Section Title"


def test_repeated_headings() -> None:
    """Test mapping of repeated headings across different pages."""
    blocks_p1 = [
        TextBlock(text="Projects", page=1, block_index=0, reading_order=0),
        TextBlock(text="Project A", page=1, block_index=1, reading_order=1),
    ]
    blocks_p2 = [
        TextBlock(text="Projects", page=2, block_index=0, reading_order=2),
        TextBlock(text="Project B", page=2, block_index=1, reading_order=3),
    ]
    pages = [
        Page(page_number=1, text_blocks=blocks_p1),
        Page(page_number=2, text_blocks=blocks_p2),
    ]
    content = _create_test_document_content(pages)

    bound_1 = SectionBoundary(
        boundary_id=uuid4(),
        heading=HeadingCandidate(
            text="Projects",
            normalized_text="projects",
            page_number=1,
            block_index=0,
            confidence=1.0,
        ),
        start_page=1,
        start_block=0,
        end_page=1,
        end_block=1,
        confidence=1.0,
    )

    bound_2 = SectionBoundary(
        boundary_id=uuid4(),
        heading=HeadingCandidate(
            text="Projects",
            normalized_text="projects",
            page_number=2,
            block_index=0,
            confidence=1.0,
        ),
        start_page=2,
        start_block=0,
        end_page=2,
        end_block=1,
        confidence=1.0,
    )

    detector = SectionDetectorService()
    sections = detector.detect_sections(content=content, boundaries=[bound_1, bound_2])

    assert len(sections) == 2
    assert sections[0].section_type == SectionType.PROJECTS
    assert sections[0].page_number == 1
    assert sections[0].content == "Projects\nProject A"

    assert sections[1].section_type == SectionType.PROJECTS
    assert sections[1].page_number == 2
    assert sections[1].content == "Projects\nProject B"


def test_empty_section() -> None:
    """Test mapping handles empty sections correctly."""
    blocks = [
        TextBlock(text="Education", page=1, block_index=0, reading_order=0),
    ]
    page = Page(page_number=1, text_blocks=blocks)
    content = _create_test_document_content([page])

    boundary = SectionBoundary(
        boundary_id=uuid4(),
        heading=HeadingCandidate(
            text="Education",
            normalized_text="education",
            page_number=1,
            block_index=0,
            confidence=1.0,
        ),
        start_page=1,
        start_block=0,
        end_page=1,
        end_block=0,
        confidence=1.0,
    )

    detector = SectionDetectorService()
    sections = detector.detect_sections(content=content, boundaries=[boundary])

    assert len(sections) == 1
    assert sections[0].section_type == SectionType.EDUCATION
    assert sections[0].content == "Education"
