"""Domain entity representing a feedback recommendation."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Recommendation:
    """Core domain business entity representing optimization suggestions from agents."""

    title: str
    description: str
    priority: str
    category: str
    expected_impact: str
    confidence: float
