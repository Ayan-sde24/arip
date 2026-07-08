"""ATS Intelligence Agent orchestration."""

from app.application.ats_agent.ats_report_builder import ATSReportBuilder
from app.application.ats_agent.ats_scorer import ATSScorer
from app.domain.entities.ats_report import ATSReport
from app.domain.entities.job_description import JobDescription
from app.domain.entities.resume import Resume
from app.domain.entities.semantic_match_report import SemanticMatchReport


class ATSAgentError(Exception):
    """Raised when ATS intelligence evaluation fails."""

    pass


class ATSAgent:
    """Agent class responsible for evaluating ATS compatibility.

    Aggregates formatting, section presence/order, profile completeness,
    and semantic keyword density analysis.
    """

    def __init__(
        self,
        scorer: ATSScorer | None = None,
        builder: ATSReportBuilder | None = None,
    ) -> None:
        self.scorer = scorer or ATSScorer()
        self.builder = builder or ATSReportBuilder()

    def evaluate(
        self,
        resume: Resume,
        job: JobDescription,
        semantic_report: SemanticMatchReport,
    ) -> ATSReport:
        """Run the ATS compatibility evaluation.

        Args:
            resume: The candidate's resume domain entity.
            job: The job description domain entity.
            semantic_report: Output of SemanticMatchReport.

        Returns:
            ATSReport domain entity with complete diagnostic details.

        Raises:
            ATSAgentError: If inputs are invalid or processing fails.
        """
        if resume is None:
            raise ATSAgentError("Resume cannot be null")
        if job is None:
            raise ATSAgentError("JobDescription cannot be null")
        if semantic_report is None:
            raise ATSAgentError("SemanticMatchReport cannot be null")

        try:
            scores_data = self.scorer.score(resume, job, semantic_report)
            missing_keywords = semantic_report.missing_keywords
            return self.builder.build(scores_data, missing_keywords)
        except Exception as exc:
            raise ATSAgentError(f"ATS Agent evaluation failed: {exc}") from exc
