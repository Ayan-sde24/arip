"""Document parser infrastructure package."""

from app.infrastructure.parser.document_reader import DocumentIntelligencePipeline
from app.infrastructure.parser.exceptions import (
    CorruptedDocxError,
    EmptyDocumentError,
    ParserError,
    ReaderFailureError,
    UnreadablePDFError,
    UnsupportedEncodingError,
)

__all__ = [
    "CorruptedDocxError",
    "DocumentIntelligencePipeline",
    "EmptyDocumentError",
    "ParserError",
    "ReaderFailureError",
    "UnreadablePDFError",
    "UnsupportedEncodingError",
]
