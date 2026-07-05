"""Domain entity representing a single page extracted from a document."""

from dataclasses import dataclass, field

from app.domain.entities.text_block import TextBlock


@dataclass(frozen=True)
class Page:
    """A single page of structured content extracted from a document.

    Attributes:
        page_number: 1-based page index within the document.
        text_blocks: Ordered list of text blocks on this page.
        raw_text: Full concatenated text of the page before cleaning.
        tables: Placeholder for future table detection results.
            Each entry is a dict describing table coordinates or content.
        images: Placeholder for future image detection metadata.
            Each entry is a dict describing image position and type.
    """

    page_number: int
    text_blocks: list[TextBlock] = field(default_factory=list)
    raw_text: str = ""
    tables: list[dict[str, object]] = field(default_factory=list)
    images: list[dict[str, object]] = field(default_factory=list)
