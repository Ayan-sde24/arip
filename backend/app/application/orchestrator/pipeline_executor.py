"""Executor carrying out execution stages of the multi-agent analysis pipeline."""

from app.application.ats_agent.ats_agent import ATSAgent
from app.application.document_analysis.document_pipeline import DocumentPipeline
from app.application.job_builder.job_integration import JobIntegration
from app.application.orchestrator.analysis_context import AnalysisContext
from app.application.recruiter_agent.recruiter_agent import RecruiterAgent
from app.application.resume_builder.resume_integration import ResumeIntegration
from app.application.resume_coach.resume_coach_agent import ResumeCoachAgent
from app.application.semantic_engine.semantic_engine import SemanticEngine
from app.domain.entities.document import Document


class PipelineExecutor:
    """Invokes builders and analysis agents sequentially with error tolerance."""

    def __init__(
        self,
        doc_pipeline: DocumentPipeline | None = None,
        resume_int: ResumeIntegration | None = None,
        job_int: JobIntegration | None = None,
        semantic_engine: SemanticEngine | None = None,
        ats_agent: ATSAgent | None = None,
        recruiter_agent: RecruiterAgent | None = None,
        coach_agent: ResumeCoachAgent | None = None,
    ) -> None:
        self.doc_pipeline = doc_pipeline or DocumentPipeline()
        self.resume_int = resume_int or ResumeIntegration()
        self.job_int = job_int or JobIntegration()
        self.semantic_engine = semantic_engine or SemanticEngine()
        self.ats_agent = ats_agent or ATSAgent()
        self.recruiter_agent = recruiter_agent or RecruiterAgent()
        self.coach_agent = coach_agent or ResumeCoachAgent()

    def execute(
        self,
        context: AnalysisContext,
        resume_doc: Document,
        resume_bytes: bytes,
        job_doc: Document,
        job_bytes: bytes,
        errors: list[str],
        warnings: list[str],
    ) -> None:
        """Execute stages sequentially, handling errors independently.

        Updates the context in-place.
        """
        # ── STAGE 1: Parse and build Resume ───────────────────────────────────
        resume_cir = None
        try:
            res_result = self.doc_pipeline.run(
                document=resume_doc, content_bytes=resume_bytes
            )
            warnings.extend(res_result.warnings)
            if not res_result.success or not res_result.cir:
                errors.extend(res_result.errors)
                errors.append("Resume DocumentIntelligence parsing failed.")
            else:
                resume_cir = res_result.cir
        except Exception as exc:
            errors.append(f"Resume DocumentIntelligence parsing error: {exc}")

        if resume_cir:
            try:
                context.resume = self.resume_int.process(resume_cir)
            except Exception as exc:
                errors.append(f"Resume build integration error: {exc}")

        # ── STAGE 2: Parse and build JobDescription ───────────────────────────
        job_cir = None
        try:
            job_result = self.doc_pipeline.run(
                document=job_doc, content_bytes=job_bytes
            )
            warnings.extend(job_result.warnings)
            if not job_result.success or not job_result.cir:
                errors.extend(job_result.errors)
                errors.append("Job Description DocumentIntelligence failed.")
            else:
                job_cir = job_result.cir
        except Exception as exc:
            errors.append(f"Job Description parsing error: {exc}")

        if job_cir:
            try:
                context.job_description = self.job_int.process(job_cir)
            except Exception as exc:
                errors.append(f"Job Description build integration error: {exc}")

        # ── STAGE 3: Semantic Engine ──────────────────────────────────────────
        if context.resume and context.job_description:
            try:
                context.semantic_report = self.semantic_engine.analyse(
                    context.resume, context.job_description
                )
            except Exception as exc:
                errors.append(f"Semantic Engine match error: {exc}")
        else:
            errors.append("Skipping Semantic Engine: missing Resume or Job.")

        # ── STAGE 4: ATS Agent ────────────────────────────────────────────────
        if context.resume and context.job_description and context.semantic_report:
            try:
                context.ats_report = self.ats_agent.evaluate(
                    context.resume,
                    context.job_description,
                    context.semantic_report,
                )
            except Exception as exc:
                errors.append(f"ATS Agent evaluation error: {exc}")
        else:
            errors.append("Skipping ATS Agent: missing prerequisites.")

        # ── STAGE 5: Recruiter Agent ──────────────────────────────────────────
        if (
            context.resume
            and context.job_description
            and context.semantic_report
            and context.ats_report
        ):
            try:
                context.recruiter_report = self.recruiter_agent.evaluate(
                    context.resume,
                    context.job_description,
                    context.semantic_report,
                    context.ats_report,
                )
            except Exception as exc:
                errors.append(f"Recruiter Agent evaluation error: {exc}")
        else:
            errors.append("Skipping Recruiter Agent: missing prerequisites.")

        # ── STAGE 6: Resume Coach / Optimization Agent ────────────────────────
        if (
            context.resume
            and context.job_description
            and context.semantic_report
            and context.ats_report
            and context.recruiter_report
        ):
            try:
                context.optimization_report = self.coach_agent.optimize(
                    context.resume,
                    context.job_description,
                    context.semantic_report,
                    context.ats_report,
                    context.recruiter_report,
                )
            except Exception as exc:
                errors.append(f"Resume Coach optimization error: {exc}")
        else:
            errors.append("Skipping Resume Coach: missing prerequisites.")
