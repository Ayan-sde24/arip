"""Model representing a section boundary within a document."""

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID

from app.application.document_analysis.heading_candidate import HeadingCandidate


@dataclass(frozen=True)
class SectionBoundary:
    """Immutable representation of a section's page and block boundaries.

    Attributes:
        boundary_id: Unique identifier for the boundary.
        heading: The heading candidate that starts this section, or None for the
            leading block.
        start_page: 1-based start page index.
        start_block: 0-based start block index on the start page.
        end_page: 1-based end page index.
        end_block: 0-based end block index on the end page.
        confidence: Combined confidence score of the boundary detection [0.0, 1.0].
        evidence: Dictionary of rule evaluations supporting this boundary.
        metadata: Arbitrary metadata associated with the boundary.
    """

    boundary_id: UUID
    heading: HeadingCandidate | None
    start_page: int
    start_block: int
    end_page: int
    end_block: int
    confidence: float
    evidence: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
