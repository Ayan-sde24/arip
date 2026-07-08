"""Project Evaluator assessing resume project details."""

import re
from typing import Any

from app.application.recruiter_agent.recruiter_rule import RecruiterEvaluationRule
from app.domain.entities.ats_report import ATSReport
from app.domain.entities.job_description import JobDescription
from app.domain.entities.resume import Resume
from app.domain.entities.semantic_match_report import SemanticMatchReport


class ProjectEvaluator(RecruiterEvaluationRule):
    """Evaluates project relevance, complexity, tech depth, impact, and links."""

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

        if not resume.projects:
            weaknesses.append("No projects listed on the resume.")
            recommendations.append(
                "Add 2-3 personal or professional projects showcasing your skills."
            )
            return {
                "score": 0.0,
                "strengths": [],
                "weaknesses": weaknesses,
                "recommendations": recommendations,
                "details": {"reason": "No projects found"},
            }

        score = 60.0  # Base score for having projects

        # 1. Project relevance (skills overlap)
        job_skills = set(
            s.lower().strip() for s in (job.required_skills + job.preferred_skills)
        )
        matched_proj_skills = 0
        for proj in resume.projects:
            for s in proj.skills:
                if s.lower().strip() in job_skills:
                    matched_proj_skills += 1

        if matched_proj_skills > 0:
            score += 10.0
            strengths.append(
                "Projects demonstrate direct relevance to required technologies."
            )
        else:
            weaknesses.append(
                "Projects do not list key technologies matching the job requirements."
            )
            recommendations.append(
                "Update projects to highlight target technologies "
                "like Python or Docker."
            )

        # 2. Technical depth and complexity
        avg_skills = sum(len(p.skills) for p in resume.projects) / len(resume.projects)
        if avg_skills >= 3.0:
            score += 10.0

        # Check for deep technologies
        deep_tech = {
            "docker",
            "kubernetes",
            "aws",
            "gcp",
            "postgresql",
            "fastapi",
            "react",
        }
        has_deep = False
        for proj in resume.projects:
            desc = (proj.description or "").lower()
            proj_s = {s.lower() for s in proj.skills}
            if proj_s & deep_tech or any(dt in desc for dt in deep_tech):
                has_deep = True
                break

        if has_deep:
            score += 10.0
            strengths.append("Projects utilize advanced technical infrastructure.")

        # 3. Business impact and metrics
        has_metrics = False
        for proj in resume.projects:
            desc = proj.description or ""
            if re.search(r"\b\d+%\b|\b\d+x\b|\b\d+ms\b", desc):
                has_metrics = True
                break

        if has_metrics:
            score += 10.0
            strengths.append("Project descriptions quantify performance and impact.")
        else:
            recommendations.append(
                "Quantify project outcomes (e.g. 'improved latency by 30%')."
            )

        # 4. Links / GitHub quality
        has_links = False
        if resume.candidate and (resume.candidate.github or resume.candidate.portfolio):
            has_links = True
        for proj in resume.projects:
            if proj.url and proj.url.strip():
                has_links = True
                break

        if has_links:
            score += 10.0
            strengths.append("Open-source or project demonstration links are provided.")
        else:
            weaknesses.append("No project or GitHub repository links provided.")
            recommendations.append(
                "Include clickable URLs or GitHub links for your projects."
            )

        score = min(100.0, score)

        return {
            "score": round(score, 2),
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommendations": recommendations,
            "details": {
                "projects_count": len(resume.projects),
                "average_skills_per_project": round(avg_skills, 2),
                "has_metrics": has_metrics,
                "has_links": has_links,
            },
        }
