"""Recruiter Intelligence Agent orchestration."""

from app.application.recruiter_agent.decision_engine import DecisionEngine
from app.application.recruiter_agent.recruiter_report_builder import (
    RecruiterReportBuilder,
)
from app.domain.entities.ats_report import ATSReport
from app.domain.entities.job_description import JobDescription
from app.domain.entities.recruiter_report import RecruiterReport
from app.domain.entities.resume import Resume
from app.domain.entities.semantic_match_report import SemanticMatchReport


class RecruiterAgentError(Exception):
    """Raised when recruiter intelligence evaluation fails."""

    pass


class RecruiterAgent:
    """Agent class simulating a recruiter's evaluation.

    Coordinates project quality, experience quality, layout readability,
    leadership evidence, and communication style assessment.
    """

    def __init__(
        self,
        decision_engine: DecisionEngine | None = None,
        builder: RecruiterReportBuilder | None = None,
    ) -> None:
        self.decision_engine = decision_engine or DecisionEngine()
        self.builder = builder or RecruiterReportBuilder()

    def evaluate(
        self,
        resume: Resume,
        job: JobDescription,
        semantic_report: SemanticMatchReport,
        ats_report: ATSReport,
    ) -> RecruiterReport:
        """Evaluate ATS and resume data to produce a RecruiterReport.

        Args:
            resume: The parsed candidate resume domain entity.
            job: The job description domain entity.
            semantic_report: Semantic match results.
            ats_report: ATS parsing and scoring diagnostic report.

        Returns:
            RecruiterReport detailing recruiting verdict, strengths, and suggestions.

        Raises:
            RecruiterAgentError: If inputs are invalid or evaluation fails.
        """
        if resume is None:
            raise RecruiterAgentError("Resume cannot be null")
        if job is None:
            raise RecruiterAgentError("JobDescription cannot be null")
        if semantic_report is None:
            raise RecruiterAgentError("SemanticMatchReport cannot be null")
        if ats_report is None:
            raise RecruiterAgentError("ATSReport cannot be null")

        try:
            decision_data = self.decision_engine.process(
                resume, job, semantic_report, ats_report
            )
            return self.builder.build(decision_data)
        except Exception as exc:
            raise RecruiterAgentError(
                f"Recruiter Agent evaluation failed: {exc}"
            ) from exc
