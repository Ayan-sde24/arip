"""DTO representing chart details for the frontend."""

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ChartResponseDTO:
    """Frontend-ready formatted chart data configurations."""

    skill_coverage: dict[str, Any] = field(default_factory=dict)
    score_breakdown: dict[str, Any] = field(default_factory=dict)
    experience_comparison: dict[str, Any] = field(default_factory=dict)
    education_comparison: dict[str, Any] = field(default_factory=dict)
    gap_analysis: dict[str, Any] = field(default_factory=dict)
