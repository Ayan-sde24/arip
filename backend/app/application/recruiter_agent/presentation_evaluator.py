"""Presentation Evaluator assessing resume readability, layout, and length."""

from typing import Any

from app.application.recruiter_agent.recruiter_rule import RecruiterEvaluationRule
from app.domain.entities.ats_report import ATSReport
from app.domain.entities.job_description import JobDescription
from app.domain.entities.resume import Resume
from app.domain.entities.semantic_match_report import SemanticMatchReport


class PresentationEvaluator(RecruiterEvaluationRule):
    """Evaluates formatting, section layout, clarity, and length appropriateness."""

    def evaluate(
        self,
        resume: Resume,
        job: JobDescription,
        semantic_report: SemanticMatchReport,
        ats_report: ATSReport,
    ) -> dict[str, Any]:
        strengths: list[str] = []
        weaknesses: list[str] = []
        recommendations: list[str] = []

        score = 60.0

        # 1. Readability & organization from ATS report
        if ats_report.format_score >= 85.0:
            score += 15.0
            strengths.append("Strong formatting structure and layout readability.")
        elif ats_report.format_score < 60.0:
            score -= 20.0
            weaknesses.append("Poor resume formatting and structural layout.")
            recommendations.append(
                "Use a clean, standard single-column resume template."
            )

        if ats_report.section_score >= 85.0:
            score += 15.0
            strengths.append("Standard logical organization and section headers.")
        elif ats_report.section_score < 60.0:
            score -= 20.0
            weaknesses.append("Non-standard section layout or missing core headers.")
        else:
            weaknesses.append("Non-standard section layout or missing core headers.")

        # 2. Length appropriateness
        # Ideal number of experiences (1-4)
        exp_count = len(resume.experience)
        if 1 <= exp_count <= 4:
            score += 10.0
            strengths.append(
                "Length of professional history is well-tailored and concise."
            )
        elif exp_count > 4:
            weaknesses.append("High number of past experiences may feel cluttered.")
            recommendations.append(
                "Limit work history to the most relevant past 3-4 roles."
            )
        else:
            weaknesses.append("Very short professional history.")

        # 3. Content clarity (duplicates check)
        # We can extract duplicates count from ats_report or compute it
        has_dups = ats_report.format_score < 100.0 and any(
            "duplicate" in w.lower() for w in ats_report.weaknesses
        )
        if not has_dups:
            score += 10.0
            strengths.append("High clarity; no duplicate section entries detected.")
        else:
            weaknesses.append("Duplicate entries present in the resume sections.")
            recommendations.append(
                "Consolidate repetitive or duplicate content entries."
            )

        # 4. Contact/links completeness
        has_full_contact = (
            resume.candidate and resume.candidate.email and resume.candidate.phone
        )

        if has_full_contact:
            score += 10.0
        else:
            recommendations.append("Ensure contact links are clear and clickable.")

        score = min(100.0, score)

        return {
            "score": round(score, 2),
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommendations": recommendations,
            "details": {
                "experiences_count": exp_count,
                "has_duplicates": has_dups,
                "has_complete_contact": has_full_contact,
            },
        }
