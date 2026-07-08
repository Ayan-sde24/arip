"""Heading detector service that detects heading candidates on document pages."""

from typing import Protocol

from app.application.document_analysis.heading_candidate import HeadingCandidate
from app.application.document_analysis.heading_rules import (
    CapitalizationRule,
    HeadingRule,
    KeywordRule,
    LengthRule,
    PositionRule,
    WhitespaceRule,
)
from app.domain.entities.document_content import DocumentContent


class HeadingDetectorProtocol(Protocol):
    """Protocol defining the interface for heading detection engines."""

    def detect(self, *, content: DocumentContent) -> list[HeadingCandidate]:
        """Detect headings in the document content.

        Args:
            content: The DocumentContent containing pages and text blocks.

        Returns:
            A list of detected HeadingCandidate models.
        """
        ...


class HeadingDetector:
    """Service class for detecting headings using configurable rules."""

    def __init__(
        self,
        rules: list[HeadingRule] | None = None,
        threshold: float = 0.6,
    ) -> None:
        """Initialize the heading detector with rules and threshold.

        Args:
            rules: Configurable rules to use, defaults to standard rule suite.
            threshold: Confidence threshold for candidates to be returned.
        """
        self.rules = (
            rules
            if rules is not None
            else [
                KeywordRule(),
                LengthRule(),
                CapitalizationRule(),
                WhitespaceRule(),
                PositionRule(),
            ]
        )
        self.threshold = threshold

    def detect(self, *, content: DocumentContent) -> list[HeadingCandidate]:
        """Evaluate all text blocks in the document content and return candidates.

        Args:
            content: The DocumentContent containing pages and text blocks.

        Returns:
            A list of detected HeadingCandidate models.
        """
        candidates: list[HeadingCandidate] = []

        for page in content.pages:
            for block in page.text_blocks:
                scores: list[float] = []
                matched_rules: list[str] = []

                for rule in self.rules:
                    result = rule.evaluate(block, page)
                    if result.score != 0.0:
                        scores.append(result.score)
                        # Use class name as rule name
                        matched_rules.append(rule.__class__.__name__)

                total_score = sum(scores)

                # Normalize total score into [0.0, 1.0] confidence
                confidence = max(0.0, min(1.0, total_score))

                if confidence >= self.threshold:
                    normalized_text = block.text.lower().strip().rstrip(":")
                    candidates.append(
                        HeadingCandidate(
                            text=block.text,
                            normalized_text=normalized_text,
                            page_number=page.page_number,
                            block_index=block.block_index,
                            confidence=round(confidence, 3),
                            matched_rule_names=matched_rules,
                        )
                    )

        return candidates
