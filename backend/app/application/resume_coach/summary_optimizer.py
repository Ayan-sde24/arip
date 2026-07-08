"""Summary Optimizer improving the professional summary using job details and LLM."""

from app.application.resume_coach.llm_provider import LLMProvider
from app.domain.entities.job_description import JobDescription
from app.domain.entities.resume import Resume


class SummaryOptimizer:
    """Optimizes the resume summary section."""

    def __init__(self, llm: LLMProvider) -> None:
        self.llm = llm

    def optimize(self, resume: Resume, job: JobDescription) -> str:
        """Improve the resume professional summary.

        Args:
            resume: Candidate resume.
            job: Job description details.

        Returns:
            Optimized summary text.
        """
        # Fetch current summary from metadata fallback
        meta = resume.document.metadata if resume.document else {}
        current_summary = meta.get("summary") or meta.get("objective") or ""

        prompt = (
            f"Job Title: {job.title}\n"
            f"Company: {job.company}\n"
            f"Current Resume Summary: {current_summary}\n"
            f"Skills: {', '.join(resume.skills)}\n"
            "Optimize this summary to match the job description requirements."
        )
        system_instruction = (
            "You are a professional resume coach. Optimize the professional "
            "summary to be concise, impactful, and aligned with the job description."
        )

        return self.llm.generate(prompt, system_instruction=system_instruction)
