"""Stage 2 of the Document Intelligence Pipeline: Layout Analyzer.

Converts raw reader output (RawDocumentData) into ordered domain Page
and TextBlock objects, preserving reading order across the document.
"""

from app.core.logger import get_logger
from app.domain.entities.page import Page
from app.domain.entities.text_block import TextBlock
from app.infrastructure.parser.models import RawDocumentData

logger = get_logger(__name__)


class LayoutAnalyzer:
    """Analyse raw document data and produce structured Page domain objects.

    Responsibilities:
    - Convert raw block dicts into immutable :class:`TextBlock` entities.
    - Assign a monotonically increasing ``reading_order`` index globally.
    - Assemble :class:`Page` entities with ordered ``text_blocks``.
    - Leave ``tables`` and ``images`` as empty placeholders for future stages.
    """

    def analyze(self, *, raw: RawDocumentData) -> list[Page]:
        """Convert :class:`RawDocumentData` into an ordered list of :class:`Page`.

        Args:
            raw: The output of a :class:`DocumentReader`.

        Returns:
            Ordered list of :class:`Page` domain objects.
        """
        logger.info(
            "Layout analysis started for {page_count} pages",
            page_count=raw.page_count,
        )
        pages: list[Page] = []
        global_reading_order = 0

        for raw_page in raw.pages:
            text_blocks: list[TextBlock] = []

            for block in raw_page.blocks:
                text = str(block.get("text", "")).strip()
                if not text:
                    continue

                raw_bbox = block.get("bbox")
                bbox: tuple[float, float, float, float] | None = None
                if (
                    raw_bbox is not None
                    and isinstance(raw_bbox, (tuple, list))
                    and len(raw_bbox) == 4
                ):
                    bbox = (
                        float(raw_bbox[0]),
                        float(raw_bbox[1]),
                        float(raw_bbox[2]),
                        float(raw_bbox[3]),
                    )

                text_blocks.append(
                    TextBlock(
                        text=text,
                        page=raw_page.page_number,
                        block_index=int(block.get("block_index", len(text_blocks))),
                        reading_order=global_reading_order,
                        bbox=bbox,
                    )
                )
                global_reading_order += 1

            pages.append(
                Page(
                    page_number=raw_page.page_number,
                    text_blocks=text_blocks,
                    raw_text=raw_page.raw_text,
                    tables=[],  # placeholder for future table extraction
                    images=[],  # placeholder for future image detection
                )
            )

        logger.info(
            "Layout analysis complete: {page_count} pages, "
            "{block_count} total text blocks",
            page_count=len(pages),
            block_count=global_reading_order,
        )
        return pages
