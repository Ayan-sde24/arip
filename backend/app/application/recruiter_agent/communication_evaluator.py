"""Communication Evaluator assessing action verbs, metrics, and writing quality."""

import re
from typing import Any

from app.application.recruiter_agent.recruiter_rule import RecruiterEvaluationRule
from app.domain.entities.ats_report import ATSReport
from app.domain.entities.job_description import JobDescription
from app.domain.entities.resume import Resume
from app.domain.entities.semantic_match_report import SemanticMatchReport


class CommunicationEvaluator(RecruiterEvaluationRule):
    """Evaluates professional writing, action verbs, and quantified achievements."""

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

        # Compile all descriptions
        desc_parts = []
        for exp in resume.experience:
            desc_parts.extend(exp.description)
        for proj in resume.projects:
            if proj.description:
                desc_parts.append(proj.description)

        full_desc = " ".join(t for t in desc_parts if t).lower()

        # 1. Action verbs check
        action_verbs = [
            "built",
            "designed",
            "implemented",
            "developed",
            "created",
            "led",
            "managed",
            "deployed",
            "integrated",
            "monitored",
            "optimized",
            "collaborated",
            "refactored",
            "accelerated",
            "architected",
        ]
        matched_verbs = [v for v in action_verbs if v in full_desc]
        if len(matched_verbs) >= 5:
            score += 15.0
            strengths.append(
                "Excellent usage of professional action verbs to describe duties."
            )
        elif len(matched_verbs) < 3:
            weaknesses.append("Passive tone or limited action verbs used.")
            recommendations.append(
                "Start description bullets with strong action verbs "
                "(e.g. 'Implemented')."
            )

        # 2. Quantified impact & achievements
        # Regex to look for percentages, currencies, or multiplier numbers
        metrics_found = len(re.findall(r"\b\d+%\b|\$\d+|\b\d+x\b|\b\d+ms\b", full_desc))
        if metrics_found >= 2:
            score += 15.0
            strengths.append(
                "Includes quantified business impact metrics and accomplishments."
            )
        else:
            weaknesses.append(
                "Lack of quantified achievements (e.g. efficiency gains "
                "or dollar impact)."
            )
            recommendations.append(
                "Add metrics, percentages, or numbers to quantify your achievements."
            )

        # 3. Professional writing style (absence of double spaces / clean bullets)
        has_double_space = "  " in full_desc
        if not has_double_space:
            score += 10.0
        else:
            weaknesses.append(
                "Detected multiple double spaces or spacing inconsistencies."
            )
            recommendations.append("Fix double spacing and alignment layout errors.")

        # 4. Bullet length readability
        all_readable = True
        for desc in desc_parts:
            if len(desc) > 300:
                all_readable = False
                break

        if all_readable and desc_parts:
            score += 10.0
            strengths.append("Clear and readable bullet points of appropriate length.")
        elif not all_readable:
            weaknesses.append("Some description bullets are too long and dense.")
            recommendations.append(
                "Keep bullet points concise (under 2-3 lines each) for readability."
            )

        score = min(100.0, score)

        return {
            "score": round(score, 2),
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommendations": recommendations,
            "details": {
                "action_verbs_count": len(matched_verbs),
                "metrics_count": metrics_found,
                "has_spacing_issues": has_double_space,
                "has_good_bullet_length": all_readable,
            },
        }
