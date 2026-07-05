"""Domain entity representing the fully structured content of a document."""

from dataclasses import dataclass, field
from typing import Any

from app.domain.entities.document import Document
from app.domain.entities.page import Page


@dataclass(frozen=True)
class DocumentContent:
    """The unified internal representation of a processed document.

    This is the canonical output of the Document Intelligence Pipeline.
    All downstream agents (parsers, matchers, evaluators) consume this
    object rather than raw file bytes.

    Attributes:
        document: The source domain Document entity with storage metadata.
        pages: Ordered list of structured Page objects.
        raw_text: Full concatenated raw text across all pages.
        clean_text: Normalised text with whitespace and control chars cleaned.
        metadata: Arbitrary key-value pairs extracted from the document
            (e.g. author, title, creation date from PDF metadata).
        language: Detected or inferred language code (e.g. ``"en"``).
            Defaults to ``"unknown"`` until a language detector is wired in.
        statistics: Computed metrics: page_count, word_count, char_count,
            avg_words_per_page.
    """

    document: Document
    pages: list[Page] = field(default_factory=list)
    raw_text: str = ""
    clean_text: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    language: str = "unknown"
    statistics: dict[str, Any] = field(default_factory=dict)
