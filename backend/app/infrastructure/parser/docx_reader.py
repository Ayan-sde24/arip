"""DOCX document reader using python-docx."""

import io
from typing import Any

from docx import Document as _open_docx  # noqa: N813
from docx.oxml.ns import qn

from app.core.logger import get_logger
from app.infrastructure.parser.exceptions import (
    CorruptedDocxError,
    EmptyDocumentError,
    ReaderFailureError,
)
from app.infrastructure.parser.models import RawDocumentData, RawPageData

logger = get_logger(__name__)


class DocxReader:
    """Read and extract structured content from DOCX documents using python-docx.

    DOCX files do not have a native concept of pages at the XML level.
    We approximate page boundaries using explicit page-break elements.
    If no page breaks are present, the entire document is treated as one page.
    """

    def read(self, *, content: bytes) -> RawDocumentData:
        """Parse DOCX bytes into structured raw page data.

        Args:
            content: Raw DOCX file bytes.

        Returns:
            A :class:`RawDocumentData` with at least one :class:`RawPageData`.

        Raises:
            CorruptedDocxError: If the bytes cannot be opened as a DOCX.
            EmptyDocumentError: If the DOCX contains no paragraph text.
            ReaderFailureError: For unexpected errors.
        """
        logger.info("DOCX reading started")
        doc = self._open(content)
        try:
            file_metadata = self._extract_core_properties(doc)
            pages = self._split_into_pages(doc)

            all_text = "\n".join(p.raw_text for p in pages)
            if not all_text.strip():
                raise EmptyDocumentError("DOCX contains no extractable text")

            logger.info(
                "DOCX reading finished: {page_count} pages",
                page_count=len(pages),
            )
            logger.info("DOCX metadata extracted")
            return RawDocumentData(pages=pages, file_metadata=file_metadata)
        except (EmptyDocumentError, CorruptedDocxError):
            raise
        except Exception as exc:
            logger.exception("Unexpected DOCX reader failure")
            raise ReaderFailureError(f"Unexpected reader failure: {exc}") from exc

    def extract_text(self, *, content: bytes) -> str:
        """Return full concatenated text from the DOCX.

        Args:
            content: Raw DOCX file bytes.

        Returns:
            Single string with all text joined by newlines.
        """
        raw = self.read(content=content)
        return "\n".join(p.raw_text for p in raw.pages)

    def extract_metadata(self, *, content: bytes) -> dict[str, Any]:
        """Extract core properties metadata from the DOCX.

        Args:
            content: Raw DOCX file bytes.

        Returns:
            Dict of metadata fields (e.g. ``title``, ``author``, ``created``).
        """
        doc = self._open(content)
        return self._extract_core_properties(doc)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _open(self, content: bytes) -> Any:  # noqa: ANN401
        """Open a DOCX from bytes, raising CorruptedDocxError on failure."""
        try:
            return _open_docx(io.BytesIO(content))
        except Exception as exc:
            raise CorruptedDocxError(f"Cannot open DOCX: {exc}") from exc

    @staticmethod
    def _has_page_break(paragraph: object) -> bool:
        """Return True if ``paragraph`` ends with an explicit page-break run."""
        for run in getattr(paragraph, "runs", []):
            for elem in run._element:  # noqa: SLF001
                if elem.tag.endswith("br") and elem.get(qn("w:type")) == "page":
                    return True
        return False

    def _split_into_pages(self, doc: Any) -> list[RawPageData]:  # noqa: ANN401
        """Split document paragraphs into approximate pages.

        Uses explicit ``w:pageBreak`` elements as page separators. If none
        exist, the entire document is returned as a single page.

        Args:
            doc: An opened python-docx ``Document`` object.

        Returns:
            Ordered list of :class:`RawPageData`, one per detected page.
        """
        pages: list[RawPageData] = []
        current_page_paragraphs: list[str] = []
        current_blocks: list[dict[str, Any]] = []
        page_number = 1

        for para in doc.paragraphs:
            text = para.text.strip()
            if text:
                block_index = len(current_blocks)
                current_page_paragraphs.append(text)
                current_blocks.append(
                    {
                        "text": text,
                        "bbox": None,
                        "block_index": block_index,
                    }
                )

            if self._has_page_break(para):
                pages.append(
                    RawPageData(
                        page_number=page_number,
                        raw_text="\n".join(current_page_paragraphs),
                        blocks=current_blocks,
                    )
                )
                page_number += 1
                current_page_paragraphs = []
                current_blocks = []

        # Append remaining content as the last page
        if current_page_paragraphs or not pages:
            pages.append(
                RawPageData(
                    page_number=page_number,
                    raw_text="\n".join(current_page_paragraphs),
                    blocks=current_blocks,
                )
            )

        return pages

    @staticmethod
    def _extract_core_properties(doc: Any) -> dict[str, Any]:  # noqa: ANN401
        """Extract built-in core properties from the DOCX.

        Args:
            doc: An opened python-docx ``Document`` object.

        Returns:
            Dict of non-None core property values.
        """
        props = doc.core_properties
        metadata: dict[str, Any] = {}
        for key in ("author", "title", "subject", "created", "modified"):
            value = getattr(props, key, None)
            if value is not None:
                metadata[key] = str(value)
        return metadata
