"""Boundary detector service that resolves section boundaries from headings."""

from typing import Any, Protocol
from uuid import uuid4

from app.application.document_analysis.boundary_rules import (
    BoundaryRule,
    EmptyLineBoundaryRule,
    EndOfDocumentBoundaryRule,
    NextHeadingBoundaryRule,
    PageBreakBoundaryRule,
    ProposedBoundary,
)
from app.application.document_analysis.heading_candidate import HeadingCandidate
from app.application.document_analysis.section_boundary import SectionBoundary
from app.domain.entities.document_content import DocumentContent


class BoundaryDetectorProtocol(Protocol):
    """Protocol defining the interface for section boundary detection engines."""

    def detect(
        self,
        *,
        content: DocumentContent,
        headings: list[HeadingCandidate],
    ) -> list[SectionBoundary]:
        """Determine section boundaries based on heading candidates.

        Args:
            content: The DocumentContent source.
            headings: Ordered HeadingCandidate list.

        Returns:
            A list of detected SectionBoundary objects.
        """
        ...


class BoundaryDetector:
    """Service class for detecting section boundaries."""

    def __init__(self, rules: list[BoundaryRule] | None = None) -> None:
        """Initialize the boundary detector with configurable rules.

        Args:
            rules: List of boundary rules, defaults to standard rule suite.
        """
        self.rules = (
            rules
            if rules is not None
            else [
                NextHeadingBoundaryRule(),
                EndOfDocumentBoundaryRule(),
                PageBreakBoundaryRule(),
                EmptyLineBoundaryRule(),
            ]
        )

    def detect(
        self,
        *,
        content: DocumentContent,
        headings: list[HeadingCandidate],
    ) -> list[SectionBoundary]:
        """Determine section boundaries based on heading candidates.

        Args:
            content: The DocumentContent source.
            headings: Ordered HeadingCandidate list.

        Returns:
            A list of detected SectionBoundary objects.
        """
        boundaries: list[SectionBoundary] = []
        if not content.pages:
            return boundaries

        # Sort headings by page and block index to ensure document order
        sorted_headings = sorted(
            headings,
            key=lambda h: (h.page_number, h.block_index),
        )

        # 1. Handle leading content before the first heading
        first_heading = sorted_headings[0] if sorted_headings else None
        if first_heading:
            # If first heading doesn't start at page 1 block 0, leading content exists
            if not (first_heading.page_number == 1 and first_heading.block_index == 0):
                # Ends right before the first heading
                end_page, end_block = self._get_previous_block(
                    content,
                    first_heading.page_number,
                    first_heading.block_index,
                )
                boundaries.append(
                    self._create_boundary(
                        content=content,
                        headings=sorted_headings,
                        heading=None,
                        start_page=1,
                        start_block=0,
                        end_page=end_page,
                        end_block=end_block,
                        next_heading=first_heading,
                    )
                )
        else:
            # No headings in document: single boundary for entire document
            last_page = len(content.pages)
            last_block = (
                len(content.pages[-1].text_blocks) - 1
                if content.pages[-1].text_blocks
                else 0
            )
            boundaries.append(
                self._create_boundary(
                    content=content,
                    headings=sorted_headings,
                    heading=None,
                    start_page=1,
                    start_block=0,
                    end_page=last_page,
                    end_block=last_block,
                    next_heading=None,
                )
            )
            return boundaries

        # 2. Handle sections starting at each heading
        for i, heading in enumerate(sorted_headings):
            start_page = heading.page_number
            start_block = heading.block_index

            # Determine proposed end page/block based on next heading or end of document
            next_heading = (
                sorted_headings[i + 1] if i + 1 < len(sorted_headings) else None
            )
            if next_heading:
                end_page, end_block = self._get_previous_block(
                    content,
                    next_heading.page_number,
                    next_heading.block_index,
                )
            else:
                end_page = len(content.pages)
                end_block = (
                    len(content.pages[-1].text_blocks) - 1
                    if content.pages[-1].text_blocks
                    else 0
                )

            boundaries.append(
                self._create_boundary(
                    content=content,
                    headings=sorted_headings,
                    heading=heading,
                    start_page=start_page,
                    start_block=start_block,
                    end_page=end_page,
                    end_block=end_block,
                    next_heading=next_heading,
                )
            )

        return boundaries

    def _get_previous_block(
        self,
        content: DocumentContent,
        page_num: int,
        block_idx: int,
    ) -> tuple[int, int]:
        """Find page and block index immediately preceding the given page/block."""
        if block_idx > 0:
            return page_num, block_idx - 1

        # If it's block 0 on page > 1, go to the previous page containing blocks
        for p in range(page_num - 1, 0, -1):
            page_obj = content.pages[p - 1]
            if page_obj.text_blocks:
                return p, len(page_obj.text_blocks) - 1

        # Fallback to current block if no previous blocks exist
        return page_num, block_idx

    def _create_boundary(
        self,
        content: DocumentContent,
        headings: list[HeadingCandidate],
        heading: HeadingCandidate | None,
        start_page: int,
        start_block: int,
        end_page: int,
        end_block: int,
        next_heading: HeadingCandidate | None,
    ) -> SectionBoundary:
        """Evaluate rules and assemble a SectionBoundary object."""
        proposed = ProposedBoundary(
            heading=heading,
            start_page=start_page,
            start_block=start_block,
            end_page=end_page,
            end_block=end_block,
        )

        evidence: dict[str, Any] = {}
        total_score = 0.0

        for rule in self.rules:
            res = rule.evaluate(proposed, content, headings, next_heading)
            evidence[rule.__class__.__name__] = {
                "score": res.score,
                "reason": res.reason,
            }
            total_score += res.score

        # Normalize confidence to [0.0, 1.0]
        confidence = max(0.0, min(1.0, total_score))

        return SectionBoundary(
            boundary_id=uuid4(),
            heading=heading,
            start_page=start_page,
            start_block=start_block,
            end_page=end_page,
            end_block=end_block,
            confidence=round(confidence, 3),
            evidence=evidence,
        )
