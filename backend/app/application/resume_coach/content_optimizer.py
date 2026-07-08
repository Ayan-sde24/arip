"""Content Optimizer improving descriptions and experience bullet points."""

from app.application.resume_coach.llm_provider import LLMProvider
from app.domain.entities.job_description import JobDescription
from app.domain.entities.resume import Resume


class ContentOptimizer:
    """Improves experience bullet points and description readability."""

    def __init__(self, llm: LLMProvider) -> None:
        self.llm = llm

    def optimize(self, resume: Resume, job: JobDescription) -> list[str]:
        """Improve the bullet points of past experiences.

        Args:
            resume: Candidate resume.
            job: Job description.

        Returns:
            List of improved bullet points.
        """
        bullets = []
        for exp in resume.experience:
            bullets.extend(exp.description)
        for proj in resume.projects:
            if proj.description:
                bullets.append(proj.description)

        if not bullets:
            # Fallback if no bullets exist
            bullets = ["Worked as developer to build software features."]

        optimized_bullets = []
        for bullet in bullets[:4]:  # Optimize up to 4 core bullets
            prompt = (
                f"Bullet: {bullet}\n"
                f"Target Job: {job.title}\n"
                "Improve this bullet point to be more professional."
            )
            system_instruction = (
                "Rewrite the bullet point using action verbs and strong "
                "professional presentation. Keep it to one line."
            )
            opt_b = self.llm.generate(prompt, system_instruction=system_instruction)
            optimized_bullets.append(opt_b)

        return optimized_bullets
