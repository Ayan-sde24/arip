"""Boundary rules for validating and scoring section boundaries in a document."""

from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.application.document_analysis.heading_candidate import HeadingCandidate
from app.domain.entities.document_content import DocumentContent


@dataclass(frozen=True)
class ProposedBoundary:
    """A proposed boundary range for evaluation by rules.

    Attributes:
        heading: The heading starting the section (None if leading content).
        start_page: 1-based page number where the section starts.
        start_block: 0-based block index where the section starts.
        end_page: 1-based page number where the section ends.
        end_block: 0-based block index where the section ends.
    """

    heading: HeadingCandidate | None
    start_page: int
    start_block: int
    end_page: int
    end_block: int


@dataclass(frozen=True)
class BoundaryRuleResult:
    """The outcome of evaluating a boundary rule.

    Attributes:
        score: The rule's evaluation score contribution.
        reason: Plain text explaining why the score was assigned.
    """

    score: float
    reason: str


class BoundaryRule(ABC):
    """Abstract base class for section boundary rules."""

    @abstractmethod
    def evaluate(
        self,
        boundary: ProposedBoundary,
        content: DocumentContent,
        headings: list[HeadingCandidate],
        next_heading: HeadingCandidate | None,
    ) -> BoundaryRuleResult:
        """Evaluate a proposed section boundary.

        Args:
            boundary: The proposed boundary range to check.
            content: The entire DocumentContent source.
            headings: Sorted list of all detected headings.
            next_heading: The heading immediately following this section (if any).

        Returns:
            A BoundaryRuleResult wrapping the score and explanation.
        """
        pass


class NextHeadingBoundaryRule(BoundaryRule):
    """Rule that verifies if a boundary ends right before the next section's heading."""

    def evaluate(
        self,
        boundary: ProposedBoundary,
        content: DocumentContent,
        headings: list[HeadingCandidate],
        next_heading: HeadingCandidate | None,
    ) -> BoundaryRuleResult:
        """Evaluate NextHeadingBoundaryRule."""
        if next_heading is None:
            return BoundaryRuleResult(0.0, "No next heading exists for this boundary")

        # Verify if proposed boundary ends right before next_heading
        # Check block preceding next_heading
        expected_page = next_heading.page_number
        expected_block = next_heading.block_index

        if expected_block > 0:
            if (
                boundary.end_page == expected_page
                and boundary.end_block == expected_block - 1
            ):
                return BoundaryRuleResult(
                    1.0,
                    (
                        f"Section ends immediately before next heading "
                        f"on page {expected_page}"
                    ),
                )
        else:
            # Expected block is 0, so it must end on the previous page containing blocks
            for prev_p in range(expected_page - 1, 0, -1):
                page_obj = content.pages[prev_p - 1]
                if page_obj.text_blocks:
                    if (
                        boundary.end_page == prev_p
                        and boundary.end_block == len(page_obj.text_blocks) - 1
                    ):
                        return BoundaryRuleResult(
                            1.0,
                            (
                                f"Section ends on page {prev_p} immediately before "
                                f"next heading starting page {expected_page}"
                            ),
                        )
                    break

        return BoundaryRuleResult(
            0.0, "Section boundary does not align immediately before the next heading"
        )


class EndOfDocumentBoundaryRule(BoundaryRule):
    """Rule that verifies if the boundary ends at the end of the document."""

    def evaluate(
        self,
        boundary: ProposedBoundary,
        content: DocumentContent,
        headings: list[HeadingCandidate],
        next_heading: HeadingCandidate | None,
    ) -> BoundaryRuleResult:
        """Evaluate EndOfDocumentBoundaryRule."""
        if next_heading is not None:
            return BoundaryRuleResult(
                0.0, "This is not the final section in the document"
            )

        if not content.pages:
            return BoundaryRuleResult(0.0, "Empty document content")

        last_page = len(content.pages)
        last_page_obj = content.pages[-1]
        last_block = (
            len(last_page_obj.text_blocks) - 1 if last_page_obj.text_blocks else 0
        )

        if boundary.end_page == last_page and boundary.end_block == last_block:
            return BoundaryRuleResult(
                1.0,
                (
                    f"Section correctly terminates at the last block "
                    f"of the last page ({last_page})"
                ),
            )

        return BoundaryRuleResult(
            0.0, "Section does not terminate at the end of the document"
        )


class PageBreakBoundaryRule(BoundaryRule):
    """Rule that scores boundaries aligning with a page break."""

    def evaluate(
        self,
        boundary: ProposedBoundary,
        content: DocumentContent,
        headings: list[HeadingCandidate],
        next_heading: HeadingCandidate | None,
    ) -> BoundaryRuleResult:
        """Evaluate PageBreakBoundaryRule."""
        if next_heading is None:
            return BoundaryRuleResult(
                0.0, "No next heading exists to align a page break"
            )

        # Proposed section ends on page P, and next heading starts on page P + 1
        # (usually at index 0)
        if (
            next_heading.page_number == boundary.end_page + 1
            and next_heading.block_index == 0
        ):
            return BoundaryRuleResult(
                0.5,
                (
                    f"Boundary correctly aligns with a page break from page "
                    f"{boundary.end_page} to {next_heading.page_number}"
                ),
            )

        return BoundaryRuleResult(
            0.0, "Section boundary does not align with a page break"
        )


class EmptyLineBoundaryRule(BoundaryRule):
    """Rule that scores boundaries separated by layout/reading order spacing gaps."""

    def evaluate(
        self,
        boundary: ProposedBoundary,
        content: DocumentContent,
        headings: list[HeadingCandidate],
        next_heading: HeadingCandidate | None,
    ) -> BoundaryRuleResult:
        """Evaluate EmptyLineBoundaryRule using reading order gap check."""
        if next_heading is None:
            return BoundaryRuleResult(0.0, "No next heading exists to measure gaps")

        try:
            end_page_obj = content.pages[boundary.end_page - 1]
            end_block_obj = end_page_obj.text_blocks[boundary.end_block]

            next_page_obj = content.pages[next_heading.page_number - 1]
            next_heading_block_obj = next_page_obj.text_blocks[next_heading.block_index]

            # If there is a reading order index gap, an empty line block was
            # filtered in pipeline
            gap = next_heading_block_obj.reading_order - end_block_obj.reading_order
            if gap > 1:
                return BoundaryRuleResult(
                    0.3,
                    f"Layout gap of {gap - 1} filtered empty blocks "
                    f"detected between sections",
                )
        except (IndexError, AttributeError):
            pass

        return BoundaryRuleResult(
            0.0, "No layout/whitespace gap detected between sections"
        )
