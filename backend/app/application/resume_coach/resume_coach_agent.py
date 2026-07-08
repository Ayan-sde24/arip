"""Resume Coach Agent orchestrating resume optimization checks."""

from app.application.resume_coach.achievement_optimizer import (
    AchievementOptimizer,
)
from app.application.resume_coach.content_optimizer import ContentOptimizer
from app.application.resume_coach.keyword_optimizer import KeywordOptimizer
from app.application.resume_coach.llm_provider import (
    LLMProvider,
    MockLLMProvider,
)
from app.application.resume_coach.optimization_engine import OptimizationEngine
from app.application.resume_coach.optimization_report_builder import (
    OptimizationReportBuilder,
)
from app.application.resume_coach.summary_optimizer import SummaryOptimizer
from app.domain.entities.ats_report import ATSReport
from app.domain.entities.job_description import JobDescription
from app.domain.entities.recruiter_report import RecruiterReport
from app.domain.entities.resume import Resume
from app.domain.entities.resume_optimization_report import (
    ResumeOptimizationReport,
)
from app.domain.entities.semantic_match_report import SemanticMatchReport


class ResumeCoachAgentError(Exception):
    """Raised when resume optimization fails."""

    pass


class ResumeCoachAgent:
    """Agent class providing resume coaching and optimization recommendations."""

    def __init__(
        self,
        llm: LLMProvider | None = None,
        summary_opt: SummaryOptimizer | None = None,
        content_opt: ContentOptimizer | None = None,
        achieve_opt: AchievementOptimizer | None = None,
        keyword_opt: KeywordOptimizer | None = None,
        engine: OptimizationEngine | None = None,
        builder: OptimizationReportBuilder | None = None,
    ) -> None:
        self.llm = llm or MockLLMProvider()
        self.summary_opt = summary_opt or SummaryOptimizer(self.llm)
        self.content_opt = content_opt or ContentOptimizer(self.llm)
        self.achieve_opt = achieve_opt or AchievementOptimizer(self.llm)
        self.keyword_opt = keyword_opt or KeywordOptimizer(self.llm)
        self.engine = engine or OptimizationEngine()
        self.builder = builder or OptimizationReportBuilder()

    def optimize(
        self,
        resume: Resume,
        job: JobDescription,
        semantic_report: SemanticMatchReport,
        ats_report: ATSReport,
        recruiter_report: RecruiterReport,
    ) -> ResumeOptimizationReport:
        """Run the optimization pipeline and return ResumeOptimizationReport.

        Args:
            resume: Candidate resume.
            job: Target job description.
            semantic_report: Semantic match analysis report.
            ats_report: ATS parsing diagnostic report.
            recruiter_report: Recruiter review report.

        Returns:
            ResumeOptimizationReport containing optimized resume and priorities.

        Raises:
            ResumeCoachAgentError: If inputs are invalid or generation fails.
        """
        if resume is None:
            raise ResumeCoachAgentError("Resume cannot be null")
        if job is None:
            raise ResumeCoachAgentError("JobDescription cannot be null")
        if semantic_report is None:
            raise ResumeCoachAgentError("SemanticMatchReport cannot be null")
        if ats_report is None:
            raise ResumeCoachAgentError("ATSReport cannot be null")
        if recruiter_report is None:
            raise ResumeCoachAgentError("RecruiterReport cannot be null")

        try:
            # 1. Run optimizers
            opt_summary = self.summary_opt.optimize(resume, job)
            opt_bullets = self.content_opt.optimize(resume, job)

            # (optional rewrite for achievements list)
            self.achieve_opt.optimize(resume, job)

            keyword_data = self.keyword_opt.optimize(resume, job, semantic_report)

            # 2. Compile aggregated recommendations and scores
            engine_data = self.engine.process(
                resume, semantic_report, ats_report, recruiter_report
            )

            # 3. Build and return final report
            return self.builder.build(
                engine_data=engine_data,
                optimized_summary=opt_summary,
                optimized_bullets=opt_bullets,
                suggested_skills=keyword_data.get("suggested_skills", []),
                suggested_keywords=keyword_data.get("suggested_keywords", []),
            )
        except Exception as exc:
            raise ResumeCoachAgentError(
                f"Resume Coach optimization failed: {exc}"
            ) from exc
