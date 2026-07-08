"""Data model holding complete or partial results of the pipeline execution."""

from dataclasses import dataclass, field

from app.domain.entities.ats_report import ATSReport
from app.domain.entities.job_description import JobDescription
from app.domain.entities.recruiter_report import RecruiterReport
from app.domain.entities.resume import Resume
from app.domain.entities.resume_optimization_report import (
    ResumeOptimizationReport,
)
from app.domain.entities.semantic_match_report import SemanticMatchReport


@dataclass(frozen=True)
class AnalysisResult:
    """Consolidated immutable analysis reports output of the orchestrator."""

    resume: Resume | None
    job_description: JobDescription | None
    semantic_report: SemanticMatchReport | None
    ats_report: ATSReport | None
    recruiter_report: RecruiterReport | None
    optimization_report: ResumeOptimizationReport | None
    execution_time: float
    status: str  # "success", "partial_success", "failed"
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
