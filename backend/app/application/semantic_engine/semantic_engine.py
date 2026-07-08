"""Top-level facade for the Semantic Intelligence Engine."""

from __future__ import annotations

from app.application.semantic_engine.semantic_matcher import SemanticMatcher
from app.domain.entities.job_description import JobDescription
from app.domain.entities.resume import Resume
from app.domain.entities.semantic_match_report import SemanticMatchReport


class SemanticEngineError(Exception):
    """Raised when the semantic engine fails to process inputs."""

    pass


class SemanticEngine:
    """Public API for the Semantic Intelligence Engine.

    Accepts a Resume and a JobDescription; returns a SemanticMatchReport.
    All matching is deterministic. Embedding-based matchers can be injected
    via SemanticMatcher without changing this interface.
    """

    def __init__(self, matcher: SemanticMatcher | None = None) -> None:
        self._matcher = matcher or SemanticMatcher()

    def analyse(self, resume: Resume, job: JobDescription) -> SemanticMatchReport:
        """Run the full semantic analysis pipeline.

        Args:
            resume: Parsed Resume domain entity.
            job: Parsed JobDescription domain entity.

        Returns:
            SemanticMatchReport.

        Raises:
            SemanticEngineError: If inputs are invalid or processing fails.
        """
        if resume is None:
            raise SemanticEngineError("Resume cannot be null")
        if job is None:
            raise SemanticEngineError("JobDescription cannot be null")
        try:
            return self._matcher.match(resume=resume, job=job)
        except Exception as exc:
            raise SemanticEngineError(f"Semantic analysis failed: {exc}") from exc
