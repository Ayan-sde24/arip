"""Keyword Optimizer suggesting missing skills, technologies, and certifications."""

from app.application.resume_coach.llm_provider import LLMProvider
from app.domain.entities.job_description import JobDescription
from app.domain.entities.resume import Resume
from app.domain.entities.semantic_match_report import SemanticMatchReport


class KeywordOptimizer:
    """Suggests keywords, missing skills, and certifications."""

    def __init__(self, llm: LLMProvider) -> None:
        self.llm = llm

    def optimize(
        self,
        resume: Resume,
        job: JobDescription,
        semantic_report: SemanticMatchReport,
    ) -> dict[str, list[str]]:
        """Suggest missing items based on job requirements and semantic match.

        Args:
            resume: Candidate resume.
            job: Job description.
            semantic_report: Semantic match report.

        Returns:
            Dict containing suggested skills, keywords, and certifications.
        """
        missing_skills = semantic_report.missing_skills
        missing_keywords = semantic_report.missing_keywords

        # Deduplicate and clean
        skills = list(dict.fromkeys(missing_skills))
        keywords = list(dict.fromkeys(missing_keywords))

        # Suggest certifications via LLM
        prompt = (
            f"Job: {job.title}\n"
            f"Skills required: {', '.join(job.required_skills)}\n"
            "Suggest 3 popular certifications for this role."
        )
        system_instruction = "Return only the certification names separated by commas."
        certs_raw = self.llm.generate(prompt, system_instruction=system_instruction)
        certs = [c.strip() for c in certs_raw.split(",") if c.strip()]

        return {
            "suggested_skills": skills,
            "suggested_keywords": keywords,
            "suggested_certifications": certs,
        }
