"""Stage 3 of the Document Intelligence Pipeline: DocumentContent Builder.

Assembles the final immutable :class:`DocumentContent` domain object from
structured pages, cleaned text, metadata, and computed statistics.
"""

from typing import Any

from app.core.logger import get_logger
from app.domain.entities.document import Document
from app.domain.entities.document_content import DocumentContent
from app.domain.entities.page import Page
from app.infrastructure.parser.utils import (
    clean_text,
    compute_statistics,
    detect_language,
)

logger = get_logger(__name__)


class DocumentContentBuilder:
    """Assemble a :class:`DocumentContent` from pipeline stage outputs.

    This builder is stateless — it derives everything from its arguments
    and has no side effects.
    """

    def build(
        self,
        *,
        document: Document,
        pages: list[Page],
        file_metadata: dict[str, Any],
    ) -> DocumentContent:
        """Construct the final :class:`DocumentContent` domain object.

        Args:
            document: The source :class:`Document` domain entity carrying
                storage-level metadata (id, filename, checksum, etc.).
            pages: Ordered list of :class:`Page` domain objects produced by
                the :class:`LayoutAnalyzer`.
            file_metadata: Header metadata extracted by the reader
                (e.g. ``title``, ``author`` from PDF/DOCX properties).

        Returns:
            An immutable :class:`DocumentContent` ready for downstream agents.
        """
        raw_text = "\n".join(page.raw_text for page in pages)
        cleaned = clean_text(raw_text)
        language = detect_language(cleaned)
        stats = compute_statistics(raw_text=raw_text, page_count=len(pages))

        logger.info(
            "DocumentContent built: {page_count} pages, "
            "{word_count} words, language={language}",
            page_count=stats.page_count,
            word_count=stats.word_count,
            language=language,
        )

        return DocumentContent(
            document=document,
            pages=pages,
            raw_text=raw_text,
            clean_text=cleaned,
            metadata=file_metadata,
            language=language,
            statistics={
                "page_count": stats.page_count,
                "word_count": stats.word_count,
                "char_count": stats.char_count,
                "avg_words_per_page": stats.avg_words_per_page,
            },
        )
