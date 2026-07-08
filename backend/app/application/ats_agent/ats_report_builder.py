"""Builder class for assembling the final ATSReport domain entity."""

from typing import Any

from app.domain.entities.ats_report import ATSReport


class ATSReportBuilder:
    """Assembles scoring results and metadata into a structured ATSReport."""

    def build(
        self,
        scores_data: dict[str, Any],
        missing_keywords: list[str],
    ) -> ATSReport:
        """Construct the ATSReport entity from raw score output.

        Args:
            scores_data: Compilation of scores, strengths, weaknesses, etc.
            missing_keywords: List of missing keywords from semantic match.

        Returns:
            Fully populated ATSReport.
        """
        overall = scores_data["overall_score"]
        format_sc = scores_data["format_score"]
        section_sc = scores_data["section_score"]

        # Parseability assessment
        if format_sc >= 80.0 and section_sc >= 80.0:
            parseability = "High"
        elif format_sc < 50.0 or section_sc < 50.0:
            parseability = "Low"
        else:
            parseability = "Medium"

        # Shortlisting probability assessment
        if overall >= 80.0:
            probability = "High"
        elif overall >= 55.0:
            probability = "Medium"
        else:
            probability = "Low"

        return ATSReport(
            overall_ats_score=overall,
            keyword_score=scores_data["keyword_score"],
            format_score=format_sc,
            section_score=section_sc,
            completeness_score=scores_data["completeness_score"],
            resume_parseability=parseability,
            ats_shortlisting_probability=probability,
            strengths=scores_data.get("strengths", []),
            weaknesses=scores_data.get("weaknesses", []),
            missing_keywords=missing_keywords,
            recommendations=scores_data.get("recommendations", []),
        )
