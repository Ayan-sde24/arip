"""Domain entity representing the standard output of an AI agent."""

from dataclasses import dataclass, field
from typing import Any

from app.domain.entities.evidence import Evidence
from app.domain.entities.recommendation import Recommendation


@dataclass(frozen=True)
class AgentResult:
    """Core domain business entity representing the execution output of an AI agent."""

    agent_name: str
    status: str
    score: float | None = None
    confidence: float | None = None
    strengths: list[str] = field(default_factory=list)
    weaknesses: list[str] = field(default_factory=list)
    recommendations: list[Recommendation] = field(default_factory=list)
    evidence: list[Evidence] = field(default_factory=list)
    execution_time: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)
