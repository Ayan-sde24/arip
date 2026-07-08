"""Experience Evaluator assessing work history details."""

import re
from typing import Any

from app.application.recruiter_agent.recruiter_rule import RecruiterEvaluationRule
from app.domain.entities.ats_report import ATSReport
from app.domain.entities.job_description import JobDescription
from app.domain.entities.resume import Resume
from app.domain.entities.semantic_match_report import SemanticMatchReport


class ExperienceEvaluator(RecruiterEvaluationRule):
    """Evaluates career progression, role relevance, tenure, and alignment."""

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

        if not resume.experience:
            weaknesses.append("Work experience section is completely missing.")
            recommendations.append("Add your professional employment history.")
            return {
                "score": 0.0,
                "strengths": [],
                "weaknesses": weaknesses,
                "recommendations": recommendations,
                "details": {"reason": "No experience found"},
            }

        score = 60.0

        # 1. Role relevance
        job_title_words = set(re.findall(r"\w+", job.title.lower()))
        matched_roles = False
        for exp in resume.experience:
            role_words = set(re.findall(r"\w+", exp.role.lower()))
            if job_title_words & role_words:
                matched_roles = True
                break

        if matched_roles:
            score += 15.0
            strengths.append(
                "Directly matching or highly relevant job roles in work history."
            )
        else:
            weaknesses.append(
                "Job titles in work history do not match the target role."
            )
            recommendations.append(
                "Highlight relevant keywords in your professional role titles."
            )

        # 2. Career progression
        seniority_keywords = [
            "senior",
            "lead",
            "principal",
            "manager",
            "architect",
            "head",
        ]
        has_progression = False
        if len(resume.experience) >= 2:
            # Check if later roles have seniority keywords and earlier ones don't
            # Assuming experience list is in reverse chronological order
            latest_role = resume.experience[0].role.lower()
            earlier_roles = [r.role.lower() for r in resume.experience[1:]]

            latest_senior = any(kw in latest_role for kw in seniority_keywords)
            earlier_senior = any(
                any(kw in r for kw in seniority_keywords) for r in earlier_roles
            )

            if latest_senior and not earlier_senior:
                has_progression = True

        if has_progression:
            score += 10.0
            strengths.append(
                "Clear career progression and promotion indicators detected."
            )

        # 3. Employment continuity / tenure
        # Average duration of each role
        avg_years = 0.0
        total_durations = 0.0
        for exp in resume.experience:
            try:
                start_m = re.search(r"\b\d{4}\b", exp.start_date or "")
                start = float(start_m.group()) if start_m else 2026.0
                end_raw = exp.end_date or ""
                if "present" in end_raw.lower() or "current" in end_raw.lower():
                    end = float(2026)
                else:
                    end_m = re.search(r"\b\d{4}\b", end_raw)
                    end = float(end_m.group()) if end_m else 2026.0
                total_durations += max(0.5, end - start)
            except Exception:
                total_durations += 1.5  # Default fallback if unparseable

        avg_years = total_durations / len(resume.experience)
        if avg_years >= 2.0:
            score += 10.0
            strengths.append("Good employment continuity and tenure at past companies.")
        elif avg_years < 1.0:
            weaknesses.append("Short job tenures (average less than 1 year).")
            recommendations.append(
                "Provide brief context if short tenures were contract positions."
            )

        # 4. Experience Quality
        has_detailed_bullets = all(
            len(exp.description) >= 3 for exp in resume.experience
        )
        if has_detailed_bullets:
            score += 10.0
            strengths.append(
                "Thorough and detailed descriptions of role responsibilities."
            )
        else:
            recommendations.append(
                "Expand descriptions to include 3-5 bullet points per position."
            )

        # 5. Industry Alignment
        job_skills = set(s.lower().strip() for s in job.required_skills)
        exp_skills_overlap = 0
        for exp in resume.experience:
            for s in exp.skills:
                if s.lower().strip() in job_skills:
                    exp_skills_overlap += 1

        if exp_skills_overlap > 1:
            score += 10.0
            strengths.append(
                "Past experience displays strong industry technology alignment."
            )

        score = min(100.0, score)

        return {
            "score": round(score, 2),
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommendations": recommendations,
            "details": {
                "average_tenure_years": round(avg_years, 2),
                "has_progression": has_progression,
                "roles_count": len(resume.experience),
            },
        }
