"""Recruiter evaluation rule interface."""

from abc import ABC, abstractmethod
from typing import Any

from app.domain.entities.ats_report import ATSReport
from app.domain.entities.job_description import JobDescription
from app.domain.entities.resume import Resume
from app.domain.entities.semantic_match_report import SemanticMatchReport


class RecruiterEvaluationRule(ABC):
    """Abstract class defining the interface for recruiter assessment evaluators."""

    @abstractmethod
    def evaluate(
        self,
        resume: Resume,
        job: JobDescription,
        semantic_report: SemanticMatchReport,
        ats_report: ATSReport,
    ) -> dict[str, Any]:
        """Evaluate a specific recruiting aspect.

        Returns:
            A dictionary containing:
                - "score": float (0.0 to 100.0)
                - "strengths": list[str]
                - "weaknesses": list[str]
                - "recommendations": list[str]
                - "details": dict[str, Any]
        """
        pass
