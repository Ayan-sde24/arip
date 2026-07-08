"""Model representing the result of running the end-to-end document pipeline."""

from dataclasses import dataclass, field

from app.domain.entities.canonical_intermediate_representation import (
    CanonicalIntermediateRepresentation,
)


@dataclass(frozen=True)
class PipelineResult:
    """Immutable output model of the DocumentPipeline execution.

    Attributes:
        success: True if the pipeline finished without throwing errors, False otherwise.
        pipeline_version: Version of the pipeline used.
        processing_time: Duration of the execution in seconds.
        cir: The generated Canonical Intermediate Representation, or None if failed.
        warnings: List of warning logs or validation alerts.
        errors: List of error messages captured during execution.
    """

    success: bool
    pipeline_version: str
    processing_time: float
    cir: CanonicalIntermediateRepresentation | None
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
