"""Pipeline for orchestrating the complete Resume building process from the CIR."""

from app.application.resume_builder.achievement_builder import (
    AchievementBuilder,
)
from app.application.resume_builder.candidate_builder import CandidateBuilder
from app.application.resume_builder.certification_builder import (
    CertificationBuilder,
)
from app.application.resume_builder.education_builder import EducationBuilder
from app.application.resume_builder.experience_builder import ExperienceBuilder
from app.application.resume_builder.project_builder import ProjectBuilder
from app.application.resume_builder.resume_assembler import ResumeAssembler
from app.application.resume_builder.resume_validator import (
    ResumeValidator,
)
from app.application.resume_builder.skill_builder import SkillBuilder
from app.domain.entities.canonical_intermediate_representation import (
    CanonicalIntermediateRepresentation,
)
from app.domain.entities.resume import Resume


class ResumePipelineError(Exception):
    """Exception raised when end-to-end Resume pipeline execution fails."""

    pass


class ResumeIntegration:
    """Orchestrates CIR conversion into a fully populated, validated Resume."""

    def __init__(
        self,
        candidate_builder: CandidateBuilder | None = None,
        education_builder: EducationBuilder | None = None,
        experience_builder: ExperienceBuilder | None = None,
        project_builder: ProjectBuilder | None = None,
        skill_builder: SkillBuilder | None = None,
        certification_builder: CertificationBuilder | None = None,
        achievement_builder: AchievementBuilder | None = None,
        assembler: ResumeAssembler | None = None,
        validator: ResumeValidator | None = None,
    ) -> None:
        """Initialize the integration pipeline with individual builders."""
        self.candidate_builder = (
            candidate_builder if candidate_builder else CandidateBuilder()
        )
        self.education_builder = (
            education_builder if education_builder else EducationBuilder()
        )
        self.experience_builder = (
            experience_builder if experience_builder else ExperienceBuilder()
        )
        self.project_builder = project_builder if project_builder else ProjectBuilder()
        self.skill_builder = skill_builder if skill_builder else SkillBuilder()
        self.certification_builder = (
            certification_builder if certification_builder else CertificationBuilder()
        )
        self.achievement_builder = (
            achievement_builder if achievement_builder else AchievementBuilder()
        )
        self.assembler = assembler if assembler else ResumeAssembler()
        self.validator = validator if validator else ResumeValidator()

    def process(
        self,
        cir: CanonicalIntermediateRepresentation,
    ) -> Resume:
        """Execute the Resume Intelligence pipeline.

        Args:
            cir: The source Canonical Intermediate Representation.

        Returns:
            A validated, fully populated Resume domain entity.

        Raises:
            ResumePipelineError: If any building or validation stage fails.
        """
        if cir is None:
            raise ResumePipelineError("CIR cannot be null")

        try:
            # 1. Build components
            candidate = self.candidate_builder.build(cir=cir)
            education = self.education_builder.build(cir=cir)
            experience = self.experience_builder.build(cir=cir)
            projects = self.project_builder.build(cir=cir)
            skills = self.skill_builder.build(cir=cir)
            certifications = self.certification_builder.build(cir=cir)
            achievements = self.achievement_builder.build(cir=cir)

            # 2. Assemble Resume
            resume = self.assembler.assemble(
                document=cir.document,
                candidate=candidate,
                education=education,
                experience=experience,
                projects=projects,
                skills=skills,
                certifications=certifications,
                achievements=achievements,
            )

            # 3. Validate Resume
            validation_result = self.validator.validate(resume)
            if not validation_result.is_valid:
                flat_errors = []
                for field_name, field_errs in validation_result.errors.items():
                    flat_errors.append(f"{field_name}: {'; '.join(field_errs)}")
                raise ResumePipelineError(
                    f"Resume cross-field validation failed: {', '.join(flat_errors)}"
                )

            return resume

        except Exception as e:
            if isinstance(e, ResumePipelineError):
                raise
            raise ResumePipelineError(f"Pipeline execution failed: {e}") from e
