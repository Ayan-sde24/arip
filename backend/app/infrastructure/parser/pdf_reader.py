"""PDF document reader using PyMuPDF (fitz)."""

from typing import Any

import fitz  # type: ignore[import-untyped]

from app.core.logger import get_logger
from app.infrastructure.parser.exceptions import (
    EmptyDocumentError,
    ReaderFailureError,
    UnreadablePDFError,
)
from app.infrastructure.parser.models import RawDocumentData, RawPageData

logger = get_logger(__name__)

# fitz block type constant for text
_FITZ_TEXT_BLOCK_TYPE = 0


class PdfReader:
    """Read and extract structured content from PDF documents using PyMuPDF.

    Uses PyMuPDF's ``get_text("dict")`` to preserve layout and bounding-box
    information per text block, enabling faithful reading-order reconstruction.
    """

    def read(self, *, content: bytes) -> RawDocumentData:
        """Parse PDF bytes into structured raw page data.

        Args:
            content: Raw PDF file bytes.

        Returns:
            A :class:`RawDocumentData` with one :class:`RawPageData` per page.

        Raises:
            UnreadablePDFError: If the bytes cannot be parsed as a PDF.
            EmptyDocumentError: If the PDF contains no extractable text.
            ReaderFailureError: For unexpected fitz-level errors.
        """
        logger.info("PDF reading started")
        doc = self._open(content)
        try:
            file_metadata = self._get_metadata(doc)
            pages: list[RawPageData] = []

            for page_index in range(len(doc)):
                page = doc[page_index]
                page_dict = page.get_text("dict")
                blocks_raw: list[dict[str, Any]] = []
                page_texts: list[str] = []

                for block in page_dict.get("blocks", []):
                    if block.get("type") != _FITZ_TEXT_BLOCK_TYPE:
                        continue
                    block_text = " ".join(
                        span.get("text", "")
                        for line in block.get("lines", [])
                        for span in line.get("spans", [])
                    ).strip()
                    if not block_text:
                        continue
                    bbox = block.get("bbox", (0.0, 0.0, 0.0, 0.0))
                    blocks_raw.append(
                        {
                            "text": block_text,
                            "bbox": tuple(bbox),
                            "block_index": len(blocks_raw),
                        }
                    )
                    page_texts.append(block_text)

                raw_page_text = "\n".join(page_texts)
                pages.append(
                    RawPageData(
                        page_number=page_index + 1,
                        raw_text=raw_page_text,
                        blocks=blocks_raw,
                    )
                )

            logger.info(
                "PDF reading finished: {page_count} pages",
                page_count=len(pages),
            )

            raw_data = RawDocumentData(pages=pages, file_metadata=file_metadata)
            all_text = "\n".join(p.raw_text for p in raw_data.pages)
            if not all_text.strip():
                raise EmptyDocumentError("PDF contains no extractable text")

            logger.info("PDF metadata extracted")
            return raw_data
        except EmptyDocumentError:
            raise
        except Exception as exc:
            logger.exception("Unexpected PDF reader failure")
            raise ReaderFailureError(f"Unexpected reader failure: {exc}") from exc
        finally:
            doc.close()

    def extract_text(self, *, content: bytes) -> str:
        """Return full concatenated text from the PDF.

        Args:
            content: Raw PDF file bytes.

        Returns:
            Single string with all text joined by newlines.
        """
        raw = self.read(content=content)
        return "\n".join(p.raw_text for p in raw.pages)

    def extract_metadata(self, *, content: bytes) -> dict[str, Any]:
        """Extract embedded PDF metadata.

        Args:
            content: Raw PDF file bytes.

        Returns:
            Dict of metadata fields (e.g. ``title``, ``author``, ``creator``).
        """
        doc = self._open(content)
        try:
            return self._get_metadata(doc)
        finally:
            doc.close()

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _open(self, content: bytes) -> fitz.Document:
        """Open a PDF from bytes, raising UnreadablePDFError on failure."""
        try:
            doc: fitz.Document = fitz.open(stream=content, filetype="pdf")
            if doc.is_closed:
                raise UnreadablePDFError("PDF document is closed after opening")
            return doc
        except fitz.FileDataError as exc:
            raise UnreadablePDFError(f"Cannot open PDF: {exc}") from exc
        except Exception as exc:
            raise UnreadablePDFError(f"Cannot open PDF: {exc}") from exc

    @staticmethod
    def _get_metadata(doc: fitz.Document) -> dict[str, Any]:
        """Extract and clean metadata from a PyMuPDF document."""
        raw: dict[str, Any] = doc.metadata or {}
        return {k: v for k, v in raw.items() if v}
