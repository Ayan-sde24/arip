"""Domain entity representing the shared execution state for analysis agents."""

from dataclasses import dataclass, field
from typing import Any

from app.domain.entities.agent_result import AgentResult
from app.domain.entities.job_description import JobDescription
from app.domain.entities.resume import Resume


@dataclass(frozen=True)
class AnalysisContext:
    """Core domain business entity holding inputs and agent results for pipelines."""

    resume: Resume
    job_description: JobDescription
    settings: dict[str, Any] = field(default_factory=dict)
    previous_agent_results: list[AgentResult] = field(default_factory=list)
    execution_metadata: dict[str, Any] = field(default_factory=dict)
