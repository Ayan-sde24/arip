"""Format scoring rule evaluating resume layout structure and data completeness."""

from typing import Any

from app.application.ats_agent.ats_rule_engine import ATSRule
from app.domain.entities.job_description import JobDescription
from app.domain.entities.resume import Resume
from app.domain.entities.semantic_match_report import SemanticMatchReport


class FormatScoreRule(ATSRule):
    """Scoring component for resume formatting and structural integrity."""

    def evaluate(
        self,
        resume: Resume,
        job: JobDescription,
        semantic_report: SemanticMatchReport,
    ) -> dict[str, Any]:
        strengths = []
        weaknesses = []
        recommendations = []

        penalties = 0.0

        # 1. Contact Information required fields
        if not resume.candidate:
            penalties += 30.0
            weaknesses.append("Missing candidate contact information section.")
            recommendations.append(
                "Add a header with name, email, phone, and professional links."
            )
        else:
            cand = resume.candidate
            if not cand.name or not cand.name.strip():
                penalties += 15.0
                weaknesses.append("Missing candidate name.")
            if not cand.email or not cand.email.strip():
                penalties += 10.0
                weaknesses.append("Missing candidate email address.")
                recommendations.append(
                    "Provide a professional email address in the contact section."
                )
            if not cand.phone or not cand.phone.strip():
                penalties += 10.0
                weaknesses.append("Missing candidate phone number.")
                recommendations.append("Provide a phone number for recruiter contact.")

        # 2. Duplicate detection (Experience, Education, Projects)
        dup_exp = 0
        seen_exp = set()
        for exp in resume.experience:
            key = (exp.company.lower().strip(), exp.role.lower().strip())
            if key in seen_exp:
                dup_exp += 1
            seen_exp.add(key)

        dup_edu = 0
        seen_edu = set()
        for edu in resume.education:
            key = (edu.institution.lower().strip(), (edu.degree or "").lower().strip())
            if key in seen_edu:
                dup_edu += 1
            seen_edu.add(key)

        dup_proj = 0
        seen_proj: set[str] = set()
        for proj in resume.projects:
            proj_key = proj.title.lower().strip()
            if proj_key in seen_proj:
                dup_proj += 1
            seen_proj.add(proj_key)

        total_dups = dup_exp + dup_edu + dup_proj
        if total_dups > 0:
            penalties += min(30.0, total_dups * 10.0)
            weaknesses.append(
                f"Detected {total_dups} duplicate entry/entries in resume sections."
            )
            recommendations.append(
                "Remove duplicate entries in experience, education, or projects."
            )

        # 3. Empty fields in entries
        empty_fields_count = 0
        for exp in resume.experience:
            if not exp.company or not exp.company.strip():
                empty_fields_count += 1
            if not exp.role or not exp.role.strip():
                empty_fields_count += 1
            if not exp.description:
                empty_fields_count += 1

        for edu in resume.education:
            if not edu.institution or not edu.institution.strip():
                empty_fields_count += 1
            if not edu.degree or not edu.degree.strip():
                empty_fields_count += 1

        for proj in resume.projects:
            if not proj.title or not proj.title.strip():
                empty_fields_count += 1

        if empty_fields_count > 0:
            penalties += min(20.0, empty_fields_count * 5.0)
            weaknesses.append(
                "Some resume entries contain incomplete required fields "
                "or empty descriptions."
            )
            recommendations.append(
                "Ensure every work experience and project has a descriptive "
                "summary and required headings."
            )

        # 4. Readable structure & organization
        # A good structure has bulleted details instead of single long paragraphs
        has_bulleted_desc = True
        for exp in resume.experience:
            if (
                exp.description
                and len(exp.description) == 1
                and len(exp.description[0]) > 200
            ):
                has_bulleted_desc = False

        if not has_bulleted_desc:
            penalties += 10.0
            weaknesses.append(
                "Work experiences contain long block paragraphs "
                "instead of bullet points."
            )
            recommendations.append(
                "Use bullet points (3-5 per role) to make experiences "
                "easy to read for ATS and recruiters."
            )

        score = max(0.0, 100.0 - penalties)
        if score >= 85.0:
            strengths.append(
                "Excellent formatting and structure; candidate details "
                "and fields are well-organized."
            )
        elif score < 60.0:
            recommendations.append(
                "Review resume layout templates for structured columns "
                "and standard headings."
            )

        return {
            "score": round(score, 2),
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommendations": recommendations,
            "details": {
                "duplicate_entries": total_dups,
                "incomplete_fields": empty_fields_count,
                "has_bulleted_descriptions": has_bulleted_desc,
            },
        }
