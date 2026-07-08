"""Optimization Engine compiling scores and recommendations across reports."""

from typing import Any

from app.domain.entities.ats_report import ATSReport
from app.domain.entities.recruiter_report import RecruiterReport
from app.domain.entities.resume import Resume
from app.domain.entities.semantic_match_report import SemanticMatchReport


class OptimizationEngine:
    """Aggregates and prioritizes optimization recommendations across all reports."""

    def process(
        self,
        resume: Resume,
        semantic_report: SemanticMatchReport,
        ats_report: ATSReport,
        recruiter_report: RecruiterReport,
    ) -> dict[str, Any]:
        """Generate score and lists of prioritized suggestions.

        Args:
            resume: Candidate resume.
            semantic_report: Semantic match report.
            ats_report: ATS compatibility report.
            recruiter_report: Recruiter review report.

        Returns:
            Dictionary containing compiled scores, priorities, and issues.
        """
        # Calculate overall optimization score:
        # 30% ATS, 40% Recruiter, 30% Semantic overall
        optimization_score = round(
            ats_report.overall_ats_score * 0.30
            + recruiter_report.overall_recruiter_score * 0.40
            + semantic_report.overall_score * 0.30,
            2,
        )

        critical_issues = []
        priority_fixes = []
        suggested_improvements = []

        # 1. Critical Issues (scores < 60, missing sections, etc.)
        if ats_report.overall_ats_score < 60.0:
            critical_issues.append("Low ATS parseability and format compatibility.")
        if recruiter_report.experience_score == 0.0:
            critical_issues.append(
                "Complete lack of professional work experience history."
            )
        if semantic_report.required_skill_coverage < 40.0:
            critical_issues.append("Critical gap in required technical skills.")

        # 2. Priority Fixes (recommendations that need urgent action)
        all_recs = (
            ats_report.recommendations
            + recruiter_report.recommendations
            + semantic_report.recommendations
        )
        # Deduplicate
        unique_recs = list(dict.fromkeys(all_recs))

        for rec in unique_recs:
            rec_l = rec.lower()
            if "missing" in rec_l or "required" in rec_l or "add " in rec_l:
                priority_fixes.append(rec)
            else:
                suggested_improvements.append(rec)

        if not priority_fixes and suggested_improvements:
            # Shift some to priority fixes if empty
            priority_fixes = suggested_improvements[:2]
            suggested_improvements = suggested_improvements[2:]

        return {
            "optimization_score": optimization_score,
            "critical_issues": critical_issues,
            "priority_fixes": priority_fixes,
            "suggested_improvements": suggested_improvements,
        }
