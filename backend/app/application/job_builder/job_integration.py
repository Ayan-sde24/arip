"""End-to-end pipeline for converting a CIR into a JobDescription."""

from app.application.job_builder.job_builder import JobBuilder
from app.application.job_builder.job_validator import JobValidationError
from app.domain.entities.canonical_intermediate_representation import (
    CanonicalIntermediateRepresentation,
)
from app.domain.entities.job_description import JobDescription


class JobPipelineError(Exception):
    """Raised when the job description pipeline fails."""

    pass


class JobIntegration:
    """Orchestrates CIR → JobDescription processing."""

    def __init__(self, builder: JobBuilder | None = None) -> None:
        self.builder = builder if builder is not None else JobBuilder()

    def process(self, cir: CanonicalIntermediateRepresentation) -> JobDescription:
        """Run the full job description pipeline.

        Args:
            cir: Source CIR.

        Returns:
            A validated JobDescription domain entity.

        Raises:
            JobPipelineError: If any stage fails.
        """
        if cir is None:
            raise JobPipelineError("CIR cannot be null")
        try:
            return self.builder.build(cir=cir)
        except JobValidationError as exc:
            raise JobPipelineError(str(exc)) from exc
        except Exception as exc:
            raise JobPipelineError(f"Pipeline execution failed: {exc}") from exc
