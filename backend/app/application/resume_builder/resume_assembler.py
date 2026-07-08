"""Assembler class for constructing immutable Resume entities."""

from app.application.resume_builder.skill_builder import Skill
from app.domain.entities.candidate import Candidate
from app.domain.entities.document import Document
from app.domain.entities.resume import (
    Achievement,
    Certification,
    Education,
    Experience,
    Project,
    Resume,
)


class ResumeAssembler:
    """Assembler responsible for combining elements into a Resume domain entity."""

    def assemble(
        self,
        *,
        document: Document,
        candidate: Candidate,
        education: list[Education],
        experience: list[Experience],
        projects: list[Project],
        skills: list[Skill],
        certifications: list[Certification],
        achievements: list[Achievement],
    ) -> Resume:
        """Combine entities into a single immutable Resume.

        Args:
            document: Source document entity.
            candidate: Candidate profile entity.
            education: List of education entities.
            experience: List of experience entities.
            projects: List of project entities.
            skills: List of Skill builder entities.
            certifications: List of certification entities.
            achievements: List of achievement entities.

        Returns:
            An assembled, immutable Resume domain entity.
        """
        # Convert Skill entities to string list for the Resume entity
        skills_str_list = [s.name for s in skills]

        return Resume(
            document=document,
            candidate=candidate,
            education=education,
            experience=experience,
            projects=projects,
            skills=skills_str_list,
            certifications=certifications,
            achievements=achievements,
        )
