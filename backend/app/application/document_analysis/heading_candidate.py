"""Model representing a heading candidate detected within a document."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class HeadingCandidate:
    """Model representing a candidate block identified as a heading.

    Attributes:
        text: The raw text of the heading block.
        normalized_text: The normalized version of the raw text for keyword comparison.
        page_number: 1-based page number where the block resides.
        confidence: Combined heuristic confidence score between 0.0 and 1.0.
        matched_rule_names: List of rule names that contributed to this
            heading candidate.
    """

    text: str
    normalized_text: str
    page_number: int
    block_index: int
    confidence: float
    matched_rule_names: list[str] = field(default_factory=list)
