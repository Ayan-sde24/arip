"""Internal value objects used within the document intelligence pipeline.

These are pipeline-private models that must not escape into the domain layer.
The pipeline converts these into proper domain entities before returning.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class RawPageData:
    """Raw text and block data extracted from a single page by a reader.

    Attributes:
        page_number: 1-based page index.
        raw_text: Full text extracted from the page.
        blocks: List of raw block dicts keyed by ``text``, ``bbox``, and
            ``block_index`` as produced by the underlying library.
    """

    page_number: int
    raw_text: str
    blocks: list[dict[str, Any]] = field(default_factory=list)


@dataclass(frozen=True)
class RawDocumentData:
    """Aggregated raw output produced by a DocumentReader.

    Attributes:
        pages: One RawPageData entry per document page.
        file_metadata: Key-value pairs extracted from the document header
            (e.g. ``title``, ``author``, ``creator`` from PDF metadata).
        page_count: Total number of pages.
    """

    pages: list[RawPageData] = field(default_factory=list)
    file_metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def page_count(self) -> int:
        """Return the number of pages extracted."""
        return len(self.pages)


@dataclass(frozen=True)
class DocumentStatistics:
    """Computed metrics about a processed document.

    Attributes:
        page_count: Total number of pages.
        word_count: Total number of whitespace-delimited words.
        char_count: Total number of characters (including spaces).
        avg_words_per_page: Average word count across pages.
    """

    page_count: int
    word_count: int
    char_count: int
    avg_words_per_page: float
