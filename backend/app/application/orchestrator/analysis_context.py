"""Orchestration context representing shared state across pipeline stages."""

from dataclasses import dataclass, field
from typing import Any

from app.domain.entities.ats_report import ATSReport
from app.domain.entities.job_description import JobDescription
from app.domain.entities.recruiter_report import RecruiterReport
from app.domain.entities.resume import Resume
from app.domain.entities.resume_optimization_report import (
    ResumeOptimizationReport,
)
from app.domain.entities.semantic_match_report import SemanticMatchReport


@dataclass
class AnalysisContext:
    """Shared workspace context for pipeline execution state."""

    resume: Resume | None = None
    job_description: JobDescription | None = None
    semantic_report: SemanticMatchReport | None = None
    ats_report: ATSReport | None = None
    recruiter_report: RecruiterReport | None = None
    optimization_report: ResumeOptimizationReport | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
