"""Rules engine for scoring and identifying document heading candidates."""

from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.domain.entities.page import Page
from app.domain.entities.text_block import TextBlock


@dataclass(frozen=True)
class RuleResult:
    """The result of evaluating a heading rule on a text block.

    Attributes:
        score: Positive or negative contribution score to the heading confidence.
        reason: Description of why the score was assigned.
    """

    score: float
    reason: str


class HeadingRule(ABC):
    """Abstract base class for heading detection rules."""

    @abstractmethod
    def evaluate(self, block: TextBlock, page: Page) -> RuleResult:
        """Evaluate a single text block within a page context.

        Args:
            block: The TextBlock entity to evaluate.
            page: The Page context containing the block.

        Returns:
            A RuleResult indicating score and evaluation reason.
        """
        pass


class LengthRule(HeadingRule):
    """Rule that scores a block based on its word count."""

    def evaluate(self, block: TextBlock, page: Page) -> RuleResult:
        """Evaluate block length."""
        words = block.text.split()
        count = len(words)
        if count == 0:
            return RuleResult(0.0, "Empty block")
        if count <= 2:
            return RuleResult(0.3, f"Very short text ({count} words)")
        if count <= 4:
            return RuleResult(0.2, f"Short text ({count} words)")
        if count <= 6:
            return RuleResult(0.1, f"Moderate length text ({count} words)")
        if count > 8:
            return RuleResult(-0.3, f"Too long for heading ({count} words)")
        return RuleResult(0.0, f"Standard text length ({count} words)")


class CapitalizationRule(HeadingRule):
    """Rule that scores a block based on its capitalization pattern."""

    def evaluate(self, block: TextBlock, page: Page) -> RuleResult:
        """Evaluate block capitalization."""
        text = block.text.strip()
        if not text:
            return RuleResult(0.0, "Empty block")

        # Check if ALL CAPS
        if text.isupper() and any(c.isalpha() for c in text):
            return RuleResult(0.3, "Text is uppercase")

        # Check if Title Case
        if text.istitle():
            return RuleResult(0.15, "Text is title case")

        return RuleResult(0.0, "Standard sentence capitalization")


class WhitespaceRule(HeadingRule):
    """Rule that scores a block based on trailing punctuation and spacing."""

    def evaluate(self, block: TextBlock, page: Page) -> RuleResult:
        """Evaluate block formatting and trailing punctuation."""
        text = block.text.strip()
        if not text:
            return RuleResult(0.0, "Empty block")

        # Check trailing punctuation
        if text.endswith(".") or text.endswith("?"):
            return RuleResult(-0.4, "Ends with sentence punctuation")

        # Check if it stands alone without list bullet punctuation
        return RuleResult(0.2, "Standalone block ending without sentence punctuation")


class KeywordRule(HeadingRule):
    """Rule that scores a block based on common section heading keywords."""

    KEYWORDS = {
        "education",
        "experience",
        "projects",
        "skills",
        "summary",
        "profile",
        "achievements",
        "languages",
        "publications",
        "certifications",
        "volunteer",
        "awards",
        "employment",
        "history",
        "contact",
        "interests",
        "hobbies",
        "objective",
    }

    def evaluate(self, block: TextBlock, page: Page) -> RuleResult:
        """Evaluate if the block contains any common section keywords."""
        # Normalize text: lowercase, remove non-alphanumeric trailing chars
        normalized = block.text.lower().strip().rstrip(":")
        # Split into words to find word matches
        words = set(normalized.split())

        if not words:
            return RuleResult(0.0, "Empty block")

        matched = words.intersection(self.KEYWORDS)
        if matched:
            return RuleResult(0.8, f"Contains heading keyword(s): {', '.join(matched)}")

        return RuleResult(0.0, "No common heading keywords matched")


class PositionRule(HeadingRule):
    """Rule that scores a block based on its position relative to other blocks."""

    def evaluate(self, block: TextBlock, page: Page) -> RuleResult:
        """Evaluate block position context relative to following text."""
        # Check if followed by a significantly longer text block
        idx = block.block_index
        if idx + 1 < len(page.text_blocks):
            next_block = page.text_blocks[idx + 1]
            # If current block is reasonably short and next block is much longer
            if len(block.text) < 40 and len(next_block.text) > 60:
                return RuleResult(0.2, "Precedes a much longer text block")

        return RuleResult(0.0, "Standard block positioning")
