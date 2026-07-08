"""Achievement Optimizer rewriting achievements for impact and clarity."""

from app.application.resume_coach.llm_provider import LLMProvider
from app.domain.entities.job_description import JobDescription
from app.domain.entities.resume import Resume


class AchievementOptimizer:
    """Optimizes achievements and awards descriptions."""

    def __init__(self, llm: LLMProvider) -> None:
        self.llm = llm

    def optimize(self, resume: Resume, job: JobDescription) -> list[str]:
        """Improve and rewrite achievements to add metrics and action verbs.

        Args:
            resume: Candidate resume.
            job: Job description.

        Returns:
            List of optimized achievements strings.
        """
        achievements_texts = []
        for ach in resume.achievements:
            achievements_texts.append(f"{ach.title}: {ach.description or ''}")

        if not achievements_texts:
            # Fallback mock achievement to suggest
            achievements_texts = [
                "Received Employee of the Month award for delivering database wrapper."
            ]

        optimized_achievements = []
        for ach_text in achievements_texts[:3]:
            prompt = (
                f"Achievement: {ach_text}\n"
                f"Target Job: {job.title}\n"
                "Rewrite this achievement to highlight quantified impact."
            )
            system_instruction = (
                "Make the achievement more impactful by incorporating hypothetical "
                "or suggested percentages, efficiency gains, and professional verbs."
            )
            opt_ach = self.llm.generate(prompt, system_instruction=system_instruction)
            optimized_achievements.append(opt_ach)

        return optimized_achievements
