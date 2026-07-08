"""Unit tests for the Heading Detection Engine (TICKET-005.2)."""

from datetime import UTC, datetime
from uuid import uuid4

from app.application.document_analysis.heading_detector import HeadingDetector
from app.domain.entities.document import Document, DocumentStatus, DocumentType
from app.domain.entities.document_content import DocumentContent
from app.domain.entities.page import Page
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


def test_detect_standard_headings() -> None:
    """Test detection of standard keyword headings (Education, Projects, Experience)."""
    blocks = [
        TextBlock(text="Education", page=1, block_index=0, reading_order=0),
        TextBlock(
            text="Graduated from MIT with a degree in EECS.",
            page=1,
            block_index=1,
            reading_order=1,
        ),
        TextBlock(text="PROJECTS", page=1, block_index=2, reading_order=2),
        TextBlock(
            text="Built a multi-agent system for resume parsing.",
            page=1,
            block_index=3,
            reading_order=3,
        ),
        TextBlock(text="Work Experience", page=1, block_index=4, reading_order=4),
        TextBlock(
            text="Senior developer at a high-tech startup.",
            page=1,
            block_index=5,
            reading_order=5,
        ),
    ]
    page = Page(page_number=1, text_blocks=blocks)
    content = _create_test_document_content([page])

    detector = HeadingDetector()
    candidates = detector.detect(content=content)

    # We expect Education, PROJECTS, and Work Experience to be headings
    assert len(candidates) == 3

    assert candidates[0].text == "Education"
    assert candidates[0].normalized_text == "education"
    assert "KeywordRule" in candidates[0].matched_rule_names

    assert candidates[1].text == "PROJECTS"
    assert candidates[1].normalized_text == "projects"
    assert "CapitalizationRule" in candidates[1].matched_rule_names

    assert candidates[2].text == "Work Experience"
    assert candidates[2].normalized_text == "work experience"


def test_detect_unknown_heading() -> None:
    """Test detection of a non-keyword heading based on positional/formatting rules."""
    blocks = [
        TextBlock(
            text="A Unique Non Keyword Header",
            page=1,
            block_index=0,
            reading_order=0,
        ),
        TextBlock(
            text="Designed and implemented a high-performance parsing pipeline "
            "handling millions of documents per day.",
            page=1,
            block_index=1,
            reading_order=1,
        ),
    ]
    page = Page(page_number=1, text_blocks=blocks)
    content = _create_test_document_content([page])

    detector = HeadingDetector()
    candidates = detector.detect(content=content)

    # "A Unique Non Keyword Header" is not a standard keyword, but should match
    # LengthRule, CapitalizationRule (Title case), WhitespaceRule (no period),
    # PositionRule.
    assert len(candidates) == 1
    assert candidates[0].text == "A Unique Non Keyword Header"
    assert "KeywordRule" not in candidates[0].matched_rule_names
    assert "PositionRule" in candidates[0].matched_rule_names


def test_detect_repeated_headings() -> None:
    """Test that multiple sections of the same type (repeated headings) are detected."""
    blocks_page1 = [
        TextBlock(text="Projects", page=1, block_index=0, reading_order=0),
        TextBlock(text="Project A details.", page=1, block_index=1, reading_order=1),
    ]
    blocks_page2 = [
        TextBlock(text="Projects", page=2, block_index=0, reading_order=2),
        TextBlock(text="Project B details.", page=2, block_index=1, reading_order=3),
    ]

    pages = [
        Page(page_number=1, text_blocks=blocks_page1),
        Page(page_number=2, text_blocks=blocks_page2),
    ]
    content = _create_test_document_content(pages)

    detector = HeadingDetector()
    candidates = detector.detect(content=content)

    assert len(candidates) == 2
    assert candidates[0].text == "Projects"
    assert candidates[0].page_number == 1
    assert candidates[1].text == "Projects"
    assert candidates[1].page_number == 2


def test_detect_lowercase_heading() -> None:
    """Test that headings written entirely in lowercase are successfully detected."""
    blocks = [
        TextBlock(text="skills", page=1, block_index=0, reading_order=0),
        TextBlock(text="Python, Rust, C++", page=1, block_index=1, reading_order=1),
    ]
    page = Page(page_number=1, text_blocks=blocks)
    content = _create_test_document_content([page])

    detector = HeadingDetector()
    candidates = detector.detect(content=content)

    assert len(candidates) == 1
    assert candidates[0].text == "skills"
    assert candidates[0].normalized_text == "skills"


def test_false_positives() -> None:
    """Test that regular prose (sentences with periods) is not detected as headings."""
    blocks = [
        TextBlock(
            text="I have worked as a developer for five years.",
            page=1,
            block_index=0,
            reading_order=0,
        ),
        TextBlock(
            text="My primary expertise lies in clean architecture.",
            page=1,
            block_index=1,
            reading_order=1,
        ),
    ]
    page = Page(page_number=1, text_blocks=blocks)
    content = _create_test_document_content([page])

    detector = HeadingDetector()
    candidates = detector.detect(content=content)

    assert len(candidates) == 0


def test_empty_document() -> None:
    """Test that an empty document returns no heading candidates."""
    content = _create_test_document_content([])

    detector = HeadingDetector()
    candidates = detector.detect(content=content)

    assert len(candidates) == 0
