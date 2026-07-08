"""Unit tests for the Section Boundary Detection Engine (TICKET-005.3)."""

from datetime import UTC, datetime
from uuid import uuid4

from app.application.document_analysis.boundary_detector import BoundaryDetector
from app.application.document_analysis.heading_candidate import HeadingCandidate
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


def test_no_headings() -> None:
    """Test document with no headings produces a single wide section boundary."""
    blocks = [
        TextBlock(text="Sentence one.", page=1, block_index=0, reading_order=0),
        TextBlock(text="Sentence two.", page=1, block_index=1, reading_order=1),
    ]
    page = Page(page_number=1, text_blocks=blocks)
    content = _create_test_document_content([page])

    detector = BoundaryDetector()
    boundaries = detector.detect(content=content, headings=[])

    assert len(boundaries) == 1
    assert boundaries[0].heading is None
    assert boundaries[0].start_page == 1
    assert boundaries[0].start_block == 0
    assert boundaries[0].end_page == 1
    assert boundaries[0].end_block == 1
    assert boundaries[0].confidence == 1.0


def test_single_section() -> None:
    """Test that one heading creates a leading section and a heading-started section."""
    blocks = [
        TextBlock(text="First Name Last Name", page=1, block_index=0, reading_order=0),
        TextBlock(text="Experience", page=1, block_index=1, reading_order=1),
        TextBlock(text="Developer at A Corp.", page=1, block_index=2, reading_order=2),
    ]
    page = Page(page_number=1, text_blocks=blocks)
    content = _create_test_document_content([page])

    headings = [
        HeadingCandidate(
            text="Experience",
            normalized_text="experience",
            page_number=1,
            block_index=1,
            confidence=1.0,
            matched_rule_names=["KeywordRule"],
        )
    ]

    detector = BoundaryDetector()
    boundaries = detector.detect(content=content, headings=headings)

    # We expect 2 boundaries:
    # 1. Leading block before first heading (heading=None, page 1 block 0
    # to page 1 block 0)
    # 2. Heading block (heading="Experience", page 1 block 1 to page 1 block 2)
    assert len(boundaries) == 2

    # Leading section
    assert boundaries[0].heading is None
    assert boundaries[0].start_page == 1
    assert boundaries[0].start_block == 0
    assert boundaries[0].end_page == 1
    assert boundaries[0].end_block == 0

    # Heading section (final section of the document)
    assert boundaries[1].heading == headings[0]
    assert boundaries[1].start_page == 1
    assert boundaries[1].start_block == 1
    assert boundaries[1].end_page == 1
    assert boundaries[1].end_block == 2
    assert "EndOfDocumentBoundaryRule" in boundaries[1].evidence
    assert boundaries[1].evidence["EndOfDocumentBoundaryRule"]["score"] == 1.0


def test_multiple_sections() -> None:
    """Test that multiple sections are correctly bounded between headings in order."""
    blocks = [
        TextBlock(text="Education", page=1, block_index=0, reading_order=0),
        TextBlock(text="MIT degree.", page=1, block_index=1, reading_order=1),
        TextBlock(text="Experience", page=1, block_index=2, reading_order=2),
        TextBlock(text="Senior Engineer.", page=1, block_index=3, reading_order=3),
    ]
    page = Page(page_number=1, text_blocks=blocks)
    content = _create_test_document_content([page])

    headings = [
        HeadingCandidate(
            text="Education",
            normalized_text="education",
            page_number=1,
            block_index=0,
            confidence=1.0,
        ),
        HeadingCandidate(
            text="Experience",
            normalized_text="experience",
            page_number=1,
            block_index=2,
            confidence=1.0,
        ),
    ]

    detector = BoundaryDetector()
    boundaries = detector.detect(content=content, headings=headings)

    # Expect 2 sections (Education, Experience). Since the first heading is at index 0,
    # there is no leading unheaded section.
    assert len(boundaries) == 2

    # Section 1: Education (starts block 0, ends block 1 right before next heading)
    assert boundaries[0].heading == headings[0]
    assert boundaries[0].start_page == 1
    assert boundaries[0].start_block == 0
    assert boundaries[0].end_page == 1
    assert boundaries[0].end_block == 1
    assert boundaries[0].evidence["NextHeadingBoundaryRule"]["score"] == 1.0

    # Section 2: Experience (starts block 2, ends block 3 at end of document)
    assert boundaries[1].heading == headings[1]
    assert boundaries[1].start_page == 1
    assert boundaries[1].start_block == 2
    assert boundaries[1].end_page == 1
    assert boundaries[1].end_block == 3
    assert boundaries[1].evidence["EndOfDocumentBoundaryRule"]["score"] == 1.0


def test_repeated_headings() -> None:
    """Test that section boundaries handle repeated headings across pages correctly."""
    blocks_p1 = [
        TextBlock(text="Projects", page=1, block_index=0, reading_order=0),
        TextBlock(text="Project A details.", page=1, block_index=1, reading_order=1),
    ]
    blocks_p2 = [
        TextBlock(text="Projects", page=2, block_index=0, reading_order=2),
        TextBlock(text="Project B details.", page=2, block_index=1, reading_order=3),
    ]
    pages = [
        Page(page_number=1, text_blocks=blocks_p1),
        Page(page_number=2, text_blocks=blocks_p2),
    ]
    content = _create_test_document_content(pages)

    headings = [
        HeadingCandidate(
            text="Projects",
            normalized_text="projects",
            page_number=1,
            block_index=0,
            confidence=1.0,
        ),
        HeadingCandidate(
            text="Projects",
            normalized_text="projects",
            page_number=2,
            block_index=0,
            confidence=1.0,
        ),
    ]

    detector = BoundaryDetector()
    boundaries = detector.detect(content=content, headings=headings)

    assert len(boundaries) == 2

    # Section 1 (starts p1 block 0, ends p1 block 1)
    assert boundaries[0].heading == headings[0]
    assert boundaries[0].start_page == 1
    assert boundaries[0].start_block == 0
    assert boundaries[0].end_page == 1
    assert boundaries[0].end_block == 1

    # Section 2 (starts p2 block 0, ends p2 block 1)
    assert boundaries[1].heading == headings[1]
    assert boundaries[1].start_page == 2
    assert boundaries[1].start_block == 0
    assert boundaries[1].end_page == 2
    assert boundaries[1].end_block == 1


def test_page_break_boundary() -> None:
    """Test that boundaries aligning with page breaks get a page break score."""
    blocks_p1 = [
        TextBlock(text="Education", page=1, block_index=0, reading_order=0),
        TextBlock(text="MIT.", page=1, block_index=1, reading_order=1),
    ]
    blocks_p2 = [
        TextBlock(text="Experience", page=2, block_index=0, reading_order=2),
        TextBlock(text="A Corp.", page=2, block_index=1, reading_order=3),
    ]
    pages = [
        Page(page_number=1, text_blocks=blocks_p1),
        Page(page_number=2, text_blocks=blocks_p2),
    ]
    content = _create_test_document_content(pages)

    headings = [
        HeadingCandidate(
            text="Education",
            normalized_text="education",
            page_number=1,
            block_index=0,
            confidence=1.0,
        ),
        HeadingCandidate(
            text="Experience",
            normalized_text="experience",
            page_number=2,
            block_index=0,
            confidence=1.0,
        ),
    ]

    detector = BoundaryDetector()
    boundaries = detector.detect(content=content, headings=headings)

    assert len(boundaries) == 2

    # Section 1 ends on page 1, next section starts on page 2 index 0
    assert boundaries[0].end_page == 1
    assert boundaries[0].end_block == 1
    assert boundaries[0].evidence["PageBreakBoundaryRule"]["score"] == 0.5
