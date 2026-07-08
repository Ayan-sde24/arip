"""Leadership Evaluator assessing ownership, initiative, mentoring, and achievements."""

from typing import Any

from app.application.recruiter_agent.recruiter_rule import RecruiterEvaluationRule
from app.domain.entities.ats_report import ATSReport
from app.domain.entities.job_description import JobDescription
from app.domain.entities.resume import Resume
from app.domain.entities.semantic_match_report import SemanticMatchReport


class LeadershipEvaluator(RecruiterEvaluationRule):
    """Evaluates evidence of leadership, mentoring, ownership, and milestones."""

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

        # Compile all text
        text_parts = []
        for exp in resume.experience:
            text_parts.append(exp.role)
            text_parts.extend(exp.description)
        for proj in resume.projects:
            text_parts.append(proj.title)
            if proj.description:
                text_parts.append(proj.description)
        for ach in resume.achievements:
            text_parts.append(ach.title)
            if ach.description:
                text_parts.append(ach.description)

        full_text = " ".join(t for t in text_parts if t).lower()

        # 1. Leadership keywords
        lead_kw = ["led", "managed", "supervised", "directed", "headed", "spearheaded"]
        has_lead = any(kw in full_text for kw in lead_kw)
        if has_lead:
            score += 10.0
            strengths.append("Demonstrated leadership and team management evidence.")
        else:
            recommendations.append(
                "Use strong action verbs like 'led' or 'spearheaded' "
                "to show leadership."
            )

        # 2. Mentoring keywords
        mentor_kw = ["mentor", "mentored", "coached", "trained", "guided", "mentoring"]
        has_mentor = any(kw in full_text for kw in mentor_kw)
        if has_mentor:
            score += 10.0
            strengths.append("Evidence of mentoring and training junior colleagues.")
        else:
            recommendations.append(
                "Include mentoring or coaching experience if you have guided others."
            )

        # 3. Ownership keywords
        ownership_kw = [
            "owned",
            "ownership",
            "responsible",
            "delivered",
            "drove",
            "solely",
        ]
        has_ownership = any(kw in full_text for kw in ownership_kw)
        if has_ownership:
            score += 10.0
            strengths.append("Shows strong task ownership and delivery focus.")

        # 4. Initiative keywords
        initiative_kw = [
            "initiative",
            "founded",
            "established",
            "created",
            "architected",
        ]
        has_initiative = any(kw in full_text for kw in initiative_kw)
        if has_initiative:
            score += 10.0
            strengths.append("Evidence of taking initiative and architectural design.")
        else:
            recommendations.append(
                "Highlight initiatives where you started or designed "
                "systems from scratch."
            )

        # 5. Achievements
        has_achievements = len(resume.achievements) > 0
        if has_achievements:
            score += 10.0
            strengths.append("Dedicated achievements or awards section listed.")
        else:
            # Achievements are optional, no penalty
            pass

        score = min(100.0, score)

        return {
            "score": round(score, 2),
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommendations": recommendations,
            "details": {
                "has_leadership_evidence": has_lead,
                "has_mentoring_evidence": has_mentor,
                "has_ownership_evidence": has_ownership,
                "has_initiative_evidence": has_initiative,
                "achievements_count": len(resume.achievements),
            },
        }
