"""Keyword scoring rule based on SemanticMatchReport and keyword density."""

import re
from typing import Any

from app.application.ats_agent.ats_rule_engine import ATSRule
from app.domain.entities.job_description import JobDescription
from app.domain.entities.resume import Resume
from app.domain.entities.semantic_match_report import SemanticMatchReport


class KeywordScoreRule(ATSRule):
    """Scoring component for keyword match and keyword density."""

    def evaluate(
        self,
        resume: Resume,
        job: JobDescription,
        semantic_report: SemanticMatchReport,
    ) -> dict[str, Any]:
        strengths = []
        weaknesses = []
        recommendations = []

        # 1. Coverage metrics from SemanticMatchReport
        req_coverage = semantic_report.required_skill_coverage
        pref_coverage = semantic_report.preferred_skill_coverage
        missing_kw = semantic_report.missing_keywords

        # Score calculations
        # Required skills coverage is critical (weight: 0.6)
        # Preferred skills coverage (weight: 0.2)
        # Keyword density score (weight: 0.2)

        # 2. Calculate keyword density
        # Assemble all text from resume
        text_parts = []
        if resume.candidate:
            text_parts.append(resume.candidate.name)
        text_parts.extend(resume.skills)
        for exp in resume.experience:
            text_parts.append(exp.role)
            text_parts.append(exp.company)
            text_parts.extend(exp.description)
            text_parts.extend(exp.skills)
        for proj in resume.projects:
            text_parts.append(proj.title)
            if proj.description:
                text_parts.append(proj.description)
            text_parts.extend(proj.skills)
        for edu in resume.education:
            text_parts.append(edu.institution)
            if edu.degree:
                text_parts.append(edu.degree)
            if edu.major:
                text_parts.append(edu.major)
            text_parts.extend(edu.details)
        for cert in resume.certifications:
            text_parts.append(cert.name)
            if cert.issuer:
                text_parts.append(cert.issuer)
        for ach in resume.achievements:
            text_parts.append(ach.title)
            if ach.description:
                text_parts.append(ach.description)

        full_resume_text = " ".join(t for t in text_parts if t).lower()
        # Tokenize by splitting non-word chars
        words = re.findall(r"\b\w+\b", full_resume_text)
        word_count = len(words)

        keyword_matches_count = 0
        job_keywords = (
            job.keywords
            if job.keywords
            else (job.required_skills + job.preferred_skills)
        )

        for kw in job_keywords:
            kw_clean = kw.lower().strip()
            if not kw_clean:
                continue
            # Find word boundaries if possible, else substring
            pattern = rf"\b{re.escape(kw_clean)}\b"
            matches = re.findall(pattern, full_resume_text)
            keyword_matches_count += len(matches)

        density = (keyword_matches_count / max(1, word_count)) * 100

        # Optimal density range is 1.5% to 10.0%
        if 1.5 <= density <= 10.0:
            density_score = 100.0
            strengths.append(f"Optimal keyword density of {density:.2f}% detected.")
        elif density < 1.5:
            # Scale down linearly
            density_score = (density / 1.5) * 100.0
            weaknesses.append(
                f"Low keyword density ({density:.2f}%). "
                "Job keywords may not be well-integrated."
            )
            recommendations.append(
                "Integrate key skills and industry terms more naturally "
                "into job descriptions and projects."
            )
        else:
            # Over-density / keyword stuffing penalty
            density_score = max(40.0, 100.0 - (density - 10.0) * 15.0)
            weaknesses.append(
                f"High keyword density ({density:.2f}%). "
                "Risk of perceived keyword stuffing."
            )
            recommendations.append(
                "Ensure keywords are used in context and avoid "
                "repetitive keyword listings."
            )

        if req_coverage >= 80.0:
            strengths.append(f"Strong required skills coverage of {req_coverage:.0f}%.")
        elif req_coverage < 50.0:
            weaknesses.append(f"Low required skills coverage of {req_coverage:.0f}%.")
            recommendations.append(
                "Add missing required skills to your resume if you "
                "have experience with them."
            )

        if missing_kw:
            recommendations.append(
                f"Incorporate missing job keywords: {', '.join(missing_kw[:5])}."
            )

        # Composite keyword score
        final_score = round(
            req_coverage * 0.6 + pref_coverage * 0.2 + density_score * 0.2, 2
        )

        return {
            "score": final_score,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommendations": recommendations,
            "details": {
                "required_coverage": req_coverage,
                "preferred_coverage": pref_coverage,
                "missing_keywords": missing_kw,
                "keyword_density_percent": round(density, 2),
                "density_score": round(density_score, 2),
            },
        }
