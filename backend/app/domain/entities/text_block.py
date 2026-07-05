"""Domain entity representing a single text block within a document page."""

from dataclasses import dataclass


@dataclass(frozen=True)
class TextBlock:
    """An ordered text fragment extracted from a single page of a document.

    Attributes:
        text: The raw text content of this block.
        page: The 1-based page number this block belongs to.
        block_index: Zero-based position of this block on the page.
        reading_order: Global reading-order index across the document.
        bbox: Optional bounding-box placeholder (x0, y0, x1, y1) in points.
            Populated for PDF; None for DOCX until layout extraction matures.
    """

    text: str
    page: int
    block_index: int
    reading_order: int
    bbox: tuple[float, float, float, float] | None = None
