"""Central orchestrator coordinating the multi-agent analysis pipeline."""

import time

from app.application.orchestrator.analysis_context import AnalysisContext
from app.application.orchestrator.analysis_result import AnalysisResult
from app.application.orchestrator.pipeline_executor import PipelineExecutor
from app.domain.entities.document import Document


class AgentOrchestrator:
    """Facade coordinating the complete multi-agent pipeline workflow."""

    def __init__(self, executor: PipelineExecutor | None = None) -> None:
        self.executor = executor or PipelineExecutor()

    def analyse(
        self,
        resume_doc: Document,
        resume_bytes: bytes,
        job_doc: Document,
        job_bytes: bytes,
    ) -> AnalysisResult:
        """Run the end-to-end multi-agent analysis pipeline.

        Args:
            resume_doc: Resume document metadata entity.
            resume_bytes: Raw parsed bytes of the resume.
            job_doc: Job description document metadata entity.
            job_bytes: Raw parsed bytes of the job description.

        Returns:
            AnalysisResult domain entity holding all reports and status.
        """
        start_time = time.perf_counter()

        context = AnalysisContext()
        errors: list[str] = []
        warnings: list[str] = []

        self.executor.execute(
            context=context,
            resume_doc=resume_doc,
            resume_bytes=resume_bytes,
            job_doc=job_doc,
            job_bytes=job_bytes,
            errors=errors,
            warnings=warnings,
        )

        # Determine status
        if not errors:
            status = "success"
        elif context.resume or context.job_description:
            status = "partial_success"
        else:
            status = "failed"

        execution_time = round(time.perf_counter() - start_time, 4)

        return AnalysisResult(
            resume=context.resume,
            job_description=context.job_description,
            semantic_report=context.semantic_report,
            ats_report=context.ats_report,
            recruiter_report=context.recruiter_report,
            optimization_report=context.optimization_report,
            execution_time=execution_time,
            status=status,
            errors=errors,
            warnings=warnings,
        )
