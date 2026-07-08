"""Section scoring rule evaluating required sections and their ordering."""

from typing import Any

from app.application.ats_agent.ats_rule_engine import ATSRule
from app.domain.entities.job_description import JobDescription
from app.domain.entities.resume import Resume
from app.domain.entities.semantic_match_report import SemanticMatchReport


class SectionScoreRule(ATSRule):
    """Scoring component for evaluating the presence and ordering of key sections."""

    def evaluate(
        self,
        resume: Resume,
        job: JobDescription,
        semantic_report: SemanticMatchReport,
    ) -> dict[str, Any]:
        strengths = []
        weaknesses = []
        recommendations = []

        # 1. Section presence check
        # Check both Resume fields and document metadata
        has_summary = False
        meta = resume.document.metadata if resume.document else {}

        # Check metadata for summary
        if (
            meta.get("has_summary")
            or meta.get("summary")
            or meta.get("objective")
            or meta.get("profile")
        ):
            has_summary = True
        elif "sections" in meta and isinstance(meta["sections"], list):
            for sec in meta["sections"]:
                sec_type = str(sec.get("section_type", "")).lower()
                sec_title = str(sec.get("title", "")).lower()
                if (
                    "summary" in sec_type
                    or "summary" in sec_title
                    or "objective" in sec_type
                    or "objective" in sec_title
                    or "profile" in sec_type
                    or "profile" in sec_title
                ):
                    has_summary = True
                    break

        has_experience = len(resume.experience) > 0
        has_education = len(resume.education) > 0
        has_skills = len(resume.skills) > 0
        has_projects = len(resume.projects) > 0
        has_certifications = len(resume.certifications) > 0

        # Section presence weights
        presence_score = 0.0
        if has_experience:
            presence_score += 25.0
        else:
            weaknesses.append("Missing Experience section.")
            recommendations.append(
                "Add a detailed Work Experience section detailing your history."
            )

        if has_education:
            presence_score += 20.0
        else:
            weaknesses.append("Missing Education section.")
            recommendations.append(
                "Add an Education section with degrees, institutions, and dates."
            )

        if has_skills:
            presence_score += 20.0
        else:
            weaknesses.append("Missing Skills section.")
            recommendations.append(
                "Add a dedicated Skills section to list core technical competencies."
            )

        if has_summary:
            presence_score += 15.0
        else:
            weaknesses.append("Missing Summary/Objective section.")
            recommendations.append(
                "Add a brief professional summary at the beginning of your resume."
            )

        if has_projects:
            presence_score += 10.0
        else:
            weaknesses.append("Missing Projects section.")
            recommendations.append(
                "Consider adding a Projects section to showcase hands-on work."
            )

        if has_certifications:
            presence_score += 10.0
        else:
            # Certifications are optional but encouraged
            pass

        # 2. Section Ordering evaluation
        # Evaluated if metadata has 'sections' list with order indices
        ordering_score = 100.0
        sections_list = meta.get("sections", [])
        if isinstance(sections_list, list) and len(sections_list) > 1:
            # We map section types to ideal order indices.
            # Ideal ranks order sections logically from Contact to Projects/Certs.
            ideal_ranks = {
                "contact": 0,
                "profile": 1,
                "summary": 1,
                "objective": 1,
                "experience": 2,
                "education": 2,
                "skills": 3,
                "projects": 4,
                "certifications": 5,
                "achievements": 5,
            }

            # Find sequence of sections as they appear
            actual_sequence = []
            for sec in sections_list:
                s_type = str(sec.get("section_type", "")).lower()
                for k, v in ideal_ranks.items():
                    if k in s_type:
                        actual_sequence.append((s_type, v))
                        break

            # Count inversions in actual sequence ranks
            inversions = 0
            for i in range(len(actual_sequence)):
                for j in range(i + 1, len(actual_sequence)):
                    if actual_sequence[i][1] > actual_sequence[j][1]:
                        inversions += 1

            if inversions > 0:
                ordering_penalty = min(30.0, inversions * 10.0)
                ordering_score -= ordering_penalty
                weaknesses.append("Sub-optimal section ordering detected.")
                recommendations.append(
                    "Order sections logically: Contact Info -> Summary -> "
                    "Experience -> Education -> Skills -> Projects."
                )

        # Composite score: 80% presence, 20% ordering
        final_score = round(presence_score * 0.8 + ordering_score * 0.2, 2)

        if final_score >= 85.0:
            strengths.append(
                "All key resume sections are present and logically ordered."
            )

        return {
            "score": final_score,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommendations": recommendations,
            "details": {
                "has_summary": has_summary,
                "has_experience": has_experience,
                "has_education": has_education,
                "has_skills": has_skills,
                "has_projects": has_projects,
                "has_certifications": has_certifications,
                "presence_score": presence_score,
                "ordering_score": ordering_score,
            },
        }
