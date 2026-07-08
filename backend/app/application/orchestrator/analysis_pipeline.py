"""Pipeline class representing the complete multi-agent analysis flow."""

from app.application.orchestrator.agent_orchestrator import AgentOrchestrator
from app.application.orchestrator.analysis_result import AnalysisResult
from app.domain.entities.document import Document


class AnalysisPipeline:
    """Configures and executes the agent analysis pipeline workflow."""

    def __init__(self, orchestrator: AgentOrchestrator | None = None) -> None:
        self.orchestrator = orchestrator or AgentOrchestrator()

    def run(
        self,
        resume_doc: Document,
        resume_bytes: bytes,
        job_doc: Document,
        job_bytes: bytes,
    ) -> AnalysisResult:
        """Run the complete pipeline flow.

        Args:
            resume_doc: Resume document entity metadata.
            resume_bytes: Raw bytes content of the resume.
            job_doc: Job description document entity metadata.
            job_bytes: Raw bytes content of the job description.

        Returns:
            The complete or partial AnalysisResult.
        """
        return self.orchestrator.analyse(
            resume_doc=resume_doc,
            resume_bytes=resume_bytes,
            job_doc=job_doc,
            job_bytes=job_bytes,
        )
