"""Builder for assembling the final ResumeOptimizationReport domain entity."""

from typing import Any

from app.domain.entities.resume_optimization_report import (
    OptimizedResume,
    ResumeOptimizationReport,
)


class OptimizationReportBuilder:
    """Assembles scoring results and optimized details into a domain report."""

    def build(
        self,
        engine_data: dict[str, Any],
        optimized_summary: str,
        optimized_bullets: list[str],
        suggested_skills: list[str],
        suggested_keywords: list[str],
    ) -> ResumeOptimizationReport:
        """Construct the ResumeOptimizationReport.

        Args:
            engine_data: Optimization engine score and recommendations.
            optimized_summary: Enhanced professional summary.
            optimized_bullets: Enhanced experience bullet points.
            suggested_skills: Missing technical skills suggestions.
            suggested_keywords: Missing keyword tags suggestions.

        Returns:
            Fully populated ResumeOptimizationReport.
        """
        opt_resume = OptimizedResume(
            summary=optimized_summary,
            bullet_points=optimized_bullets,
            suggested_skills=suggested_skills,
            suggested_keywords=suggested_keywords,
        )

        return ResumeOptimizationReport(
            optimization_score=engine_data["optimization_score"],
            priority_fixes=engine_data.get("priority_fixes", []),
            critical_issues=engine_data.get("critical_issues", []),
            suggested_improvements=engine_data.get("suggested_improvements", []),
            optimized_resume=opt_resume,
        )
