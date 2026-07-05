"""Document Intelligence Pipeline — main orchestrator (Stage 1 → 2 → 3).

Usage::

    from app.infrastructure.parser.document_reader import DocumentIntelligencePipeline

    pipeline = DocumentIntelligencePipeline()
    content = pipeline.run(document=doc, content_bytes=raw_bytes)

The pipeline selects the correct reader based on ``document.extension``,
delegates to the layout analyzer and builder, and returns an immutable
:class:`~app.domain.entities.document_content.DocumentContent`.
"""

from app.core.logger import get_logger
from app.domain.entities.document import Document
from app.domain.entities.document_content import DocumentContent
from app.infrastructure.parser.document_content_builder import DocumentContentBuilder
from app.infrastructure.parser.docx_reader import DocxReader
from app.infrastructure.parser.exceptions import ReaderFailureError
from app.infrastructure.parser.layout_analyzer import LayoutAnalyzer
from app.infrastructure.parser.models import RawDocumentData
from app.infrastructure.parser.pdf_reader import PdfReader

logger = get_logger(__name__)

_READER_REGISTRY: dict[str, type[PdfReader] | type[DocxReader]] = {
    "pdf": PdfReader,
    "docx": DocxReader,
}


class DocumentIntelligencePipeline:
    """Three-stage pipeline: Read → Analyse Layout → Build DocumentContent.

    The pipeline is stateless and thread-safe. A single instance can be
    reused across multiple documents.

    Supported extensions (Stage 1 readers):
    - ``pdf``  → :class:`~app.infrastructure.parser.pdf_reader.PdfReader`
    - ``docx`` → :class:`~app.infrastructure.parser.docx_reader.DocxReader`

    Future readers (OCR, HTML, Markdown, LinkedIn export) are registered by
    extending ``_READER_REGISTRY`` without changing this class or callers.
    """

    def __init__(self) -> None:
        """Initialise pipeline with layout analyzer and content builder."""
        self._layout_analyzer = LayoutAnalyzer()
        self._builder = DocumentContentBuilder()

    def run(
        self,
        *,
        document: Document,
        content_bytes: bytes,
    ) -> DocumentContent:
        """Execute the full pipeline for a single document.

        Args:
            document: The :class:`~app.domain.entities.document.Document`
                carrying storage metadata (extension, filename, etc.).
            content_bytes: Raw file bytes to parse.

        Returns:
            Immutable :class:`~app.domain.entities.document_content.DocumentContent`.

        Raises:
            ReaderFailureError: If no reader is registered for the extension.
            UnreadablePDFError: Propagated from :class:`PdfReader`.
            CorruptedDocxError: Propagated from :class:`DocxReader`.
            EmptyDocumentError: Propagated from any reader.
        """
        extension = document.extension.lower()
        logger.info(
            "Pipeline started for {filename} (extension={extension})",
            filename=document.original_filename,
            extension=extension,
        )

        reader_cls = _READER_REGISTRY.get(extension)
        if reader_cls is None:
            raise ReaderFailureError(
                f"No reader registered for extension '{extension}'. "
                f"Supported: {sorted(_READER_REGISTRY)}"
            )

        # Stage 1 — Read
        reader = reader_cls()
        raw: RawDocumentData = reader.read(content=content_bytes)

        # Stage 2 — Layout Analysis
        pages = self._layout_analyzer.analyze(raw=raw)

        # Stage 3 — Build DocumentContent
        result = self._builder.build(
            document=document,
            pages=pages,
            file_metadata=raw.file_metadata,
        )

        logger.info(
            "Pipeline completed for {filename}: "
            "{page_count} pages, {word_count} words",
            filename=document.original_filename,
            page_count=result.statistics.get("page_count", 0),
            word_count=result.statistics.get("word_count", 0),
        )
        return result
