"""Protocol interface for document readers in the intelligence pipeline.

Defining the interface here (not in application/) is correct because
this is an infrastructure-internal contract — the pipeline orchestrator
selects and calls readers, and nothing outside infrastructure uses them.
"""

from typing import Any, Protocol

from app.infrastructure.parser.models import RawDocumentData


class DocumentReader(Protocol):
    """Read raw content from a document file of a specific format.

    Every concrete reader (PDF, DOCX, future HTML/OCR) must implement
    this protocol so the pipeline orchestrator remains format-agnostic.
    """

    def read(self, *, content: bytes) -> RawDocumentData:
        """Parse ``content`` bytes into raw page and metadata structures.

        Args:
            content: Raw bytes of the document file.

        Returns:
            A :class:`RawDocumentData` instance with pages and metadata.

        Raises:
            UnreadablePDFError: If a PDF cannot be opened.
            CorruptedDocxError: If a DOCX cannot be opened.
            EmptyDocumentError: If the document contains no text.
            ReaderFailureError: For any unexpected reader error.
        """
        ...

    def extract_text(self, *, content: bytes) -> str:
        """Return the full concatenated raw text from the document.

        Args:
            content: Raw bytes of the document file.

        Returns:
            A single string containing all text, page-separated.
        """
        ...

    def extract_metadata(self, *, content: bytes) -> dict[str, Any]:
        """Extract header or embedded metadata from the document.

        Args:
            content: Raw bytes of the document file.

        Returns:
            A dict of metadata key-value pairs (e.g. ``author``, ``title``).
        """
        ...
