"""Builder class for assembling the final RecruiterReport domain entity."""

from typing import Any

from app.domain.entities.recruiter_report import RecruiterReport


class RecruiterReportBuilder:
    """Assembles evaluations and aggregated outputs into a RecruiterReport."""

    def build(self, decision_data: dict[str, Any]) -> RecruiterReport:
        """Construct the RecruiterReport from raw aggregated decision data.

        Args:
            decision_data: Output of the decision engine's evaluation compilation.

        Returns:
            Fully populated RecruiterReport.
        """
        reasons = []
        verdict = decision_data["recruiter_verdict"]
        overall = decision_data["overall_score"]

        # Formulate core reason messages
        reasons.append(f"Recruiter overall evaluation score is {overall:.1f}%.")
        reasons.append(f"Verdict recommendation is: '{verdict}'.")
        if decision_data.get("key_concerns"):
            reasons.append(
                f"Identified concerns: {'; '.join(decision_data['key_concerns'][:2])}."
            )
        if decision_data.get("standout_factors"):
            factors_str = "; ".join(decision_data["standout_factors"][:2])
            reasons.append(f"Standout strengths: {factors_str}.")

        return RecruiterReport(
            overall_recruiter_score=overall,
            project_score=decision_data["project_score"],
            experience_score=decision_data["experience_score"],
            presentation_score=decision_data["presentation_score"],
            leadership_score=decision_data["leadership_score"],
            communication_score=decision_data["communication_score"],
            shortlist_probability=decision_data["shortlist_probability"],
            recruiter_verdict=verdict,
            reasons=reasons,
            recommendations=decision_data.get("recommendations", []),
            strengths=decision_data.get("strengths", []),
            weaknesses=decision_data.get("weaknesses", []),
            key_concerns=decision_data.get("key_concerns", []),
            standout_factors=decision_data.get("standout_factors", []),
            improvement_suggestions=decision_data.get("recommendations", []),
        )
