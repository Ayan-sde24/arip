"""Domain entity representing audit/analysis evidence."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Evidence:
    """Core domain business entity holding trace evidence for Explainable AI."""

    title: str
    description: str
    source: str
    confidence: float
    location: str | None = None
