"""Completeness scoring rule for contact, education, experience, and skills."""

from typing import Any

from app.application.ats_agent.ats_rule_engine import ATSRule
from app.domain.entities.job_description import JobDescription
from app.domain.entities.resume import Resume
from app.domain.entities.semantic_match_report import SemanticMatchReport


class CompletenessScoreRule(ATSRule):
    """Scoring component for profile completeness."""

    def evaluate(
        self,
        resume: Resume,
        job: JobDescription,
        semantic_report: SemanticMatchReport,
    ) -> dict[str, Any]:
        strengths = []
        weaknesses = []
        recommendations = []

        # 1. Contact completeness (20%)
        contact_score = 0.0
        if resume.candidate:
            cand = resume.candidate
            if cand.name and cand.name.strip():
                contact_score += 20.0
            if cand.email and cand.email.strip():
                contact_score += 20.0
            if cand.phone and cand.phone.strip():
                contact_score += 20.0
            if cand.location and cand.location.strip():
                contact_score += 20.0
            if (
                (cand.linkedin and cand.linkedin.strip())
                or (cand.github and cand.github.strip())
                or (cand.portfolio and cand.portfolio.strip())
            ):
                contact_score += 20.0

        if contact_score < 80.0:
            weaknesses.append(
                "Contact details are incomplete (e.g. missing links or location)."
            )
            recommendations.append(
                "Add your LinkedIn, GitHub, or portfolio link, and "
                "location to your header."
            )

        # 2. Experience completeness (30%)
        exp_score = 0.0
        if resume.experience:
            # Check description presence and number of roles
            has_desc_all = all(len(e.description) > 0 for e in resume.experience)
            if len(resume.experience) >= 2:
                exp_score = 100.0 if has_desc_all else 70.0
            else:
                exp_score = 80.0 if has_desc_all else 50.0
        else:
            weaknesses.append("Zero work experience history found.")
            recommendations.append(
                "Ensure your work experience details roles, responsibilities, "
                "and achievements."
            )

        # 3. Education completeness (20%)
        edu_score = 0.0
        if resume.education:
            has_degree_major = all((e.degree and e.major) for e in resume.education)
            edu_score = 100.0 if has_degree_major else 70.0
        else:
            weaknesses.append("No educational qualifications listed.")
            recommendations.append(
                "List your highest degrees, universities, and majors."
            )

        # 4. Skills completeness (20%)
        skills_count = len(resume.skills)
        if skills_count >= 8:
            skills_score = 100.0
        elif skills_count >= 5:
            skills_score = 80.0
        elif skills_count >= 1:
            skills_score = 50.0
            weaknesses.append(f"Very few skills listed ({skills_count}).")
            recommendations.append(
                "Expand your skills list to include more technical "
                "and tool competencies."
            )
        else:
            skills_score = 0.0
            weaknesses.append("Skills section is empty.")
            recommendations.append("Add a list of technical skills to the resume.")

        # 5. Projects completeness (10%)
        proj_count = len(resume.projects)
        if proj_count >= 2:
            proj_score = 100.0
        elif proj_count == 1:
            proj_score = 80.0
        else:
            proj_score = 40.0
            # Projects are optional but good
            recommendations.append(
                "Add 1 or 2 projects to demonstrate practical application of skills."
            )

        # Aggregate weighted score
        final_score = round(
            contact_score * 0.20
            + exp_score * 0.30
            + edu_score * 0.20
            + skills_score * 0.20
            + proj_score * 0.10,
            2,
        )

        if final_score >= 90.0:
            strengths.append(
                "High overall resume completeness across all core dimensions."
            )

        return {
            "score": final_score,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommendations": recommendations,
            "details": {
                "contact_completeness_score": contact_score,
                "experience_completeness_score": exp_score,
                "education_completeness_score": edu_score,
                "skills_completeness_score": skills_score,
                "projects_completeness_score": proj_score,
            },
        }
