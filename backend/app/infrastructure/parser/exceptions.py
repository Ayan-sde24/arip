"""Custom exceptions raised by the document intelligence pipeline."""


class ParserError(Exception):
    """Base exception for all document parser failures."""


class UnreadablePDFError(ParserError):
    """Raised when a PDF file cannot be opened or decoded by the reader."""


class CorruptedDocxError(ParserError):
    """Raised when a DOCX file is structurally invalid or cannot be opened."""


class EmptyDocumentError(ParserError):
    """Raised when a document contains no extractable text content."""


class UnsupportedEncodingError(ParserError):
    """Raised when text content cannot be decoded due to an unknown encoding."""


class ReaderFailureError(ParserError):
    """Raised for unexpected reader-level failures not covered by specific errors."""
