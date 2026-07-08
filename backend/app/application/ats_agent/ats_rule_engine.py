"""Rule engine and interface for ATS compatibility analysis."""

from abc import ABC, abstractmethod
from typing import Any

from app.domain.entities.job_description import JobDescription
from app.domain.entities.resume import Resume
from app.domain.entities.semantic_match_report import SemanticMatchReport


class ATSRule(ABC):
    """Abstract interface for all ATS evaluation rules.

    This allows plug-in of alternative scoring strategies (e.g. AI-based)
    in the future without changing the caller interface.
    """

    @abstractmethod
    def evaluate(
        self,
        resume: Resume,
        job: JobDescription,
        semantic_report: SemanticMatchReport,
    ) -> dict[str, Any]:
        """Evaluate a specific ATS aspect of the resume against the job description.

        Args:
            resume: The candidate's resume entity.
            job: The job description entity.
            semantic_report: Semantic analysis report.

        Returns:
            A dictionary containing:
                - "score": float (0.0 to 100.0)
                - "strengths": list[str]
                - "weaknesses": list[str]
                - "recommendations": list[str]
                - "details": dict[str, Any] (any additional rule-specific data)
        """
        pass


class ATSRuleEngine:
    """Executes a list of ATSRules and aggregates their results."""

    def __init__(self, rules: list[ATSRule]) -> None:
        self.rules = rules

    def run(
        self,
        resume: Resume,
        job: JobDescription,
        semantic_report: SemanticMatchReport,
    ) -> list[dict[str, Any]]:
        """Run all registered rules against the inputs."""
        results = []
        for rule in self.rules:
            res = rule.evaluate(resume, job, semantic_report)
            results.append(res)
        return results
