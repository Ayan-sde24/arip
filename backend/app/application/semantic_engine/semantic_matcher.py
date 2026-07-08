"""SemanticMatcher: orchestrates all individual matchers into a single match report."""

from __future__ import annotations

from app.application.semantic_engine.education_matcher import EducationMatcher
from app.application.semantic_engine.experience_matcher import ExperienceMatcher
from app.application.semantic_engine.gap_analyzer import GapAnalyzer
from app.application.semantic_engine.keyword_matcher import KeywordMatcher
from app.application.semantic_engine.semantic_report_builder import (
    SemanticReportBuilder,
)
from app.application.semantic_engine.skill_matcher import SkillMatcher
from app.domain.entities.job_description import JobDescription
from app.domain.entities.resume import Resume
from app.domain.entities.semantic_match_report import SemanticMatchReport


class SemanticMatcher:
    """Coordinates all matchers and produces a SemanticMatchReport.

    Each matcher is injected to allow future substitution of
    embedding-based strategies without public API changes.
    """

    def __init__(
        self,
        skill_matcher: SkillMatcher | None = None,
        experience_matcher: ExperienceMatcher | None = None,
        education_matcher: EducationMatcher | None = None,
        keyword_matcher: KeywordMatcher | None = None,
        gap_analyzer: GapAnalyzer | None = None,
        report_builder: SemanticReportBuilder | None = None,
    ) -> None:
        self._skill = skill_matcher or SkillMatcher()
        self._experience = experience_matcher or ExperienceMatcher()
        self._education = education_matcher or EducationMatcher()
        self._keyword = keyword_matcher or KeywordMatcher()
        self._gap = gap_analyzer or GapAnalyzer()
        self._builder = report_builder or SemanticReportBuilder()

    def match(
        self,
        resume: Resume,
        job: JobDescription,
    ) -> SemanticMatchReport:
        """Run all match components and return a full SemanticMatchReport.

        Args:
            resume: Parsed Resume domain entity.
            job: Parsed JobDescription domain entity.

        Returns:
            SemanticMatchReport with scores, evidence, gap summary and recommendations.
        """
        skill_result = self._skill.match(
            resume_skills=resume.skills,
            required_skills=job.required_skills,
            preferred_skills=job.preferred_skills,
        )

        experience_result = self._experience.match(
            experience_list=resume.experience,
            experience_required=job.experience_required,
            required_skills=job.required_skills,
            job_title=job.title,
        )

        education_result = self._education.match(
            education_list=resume.education,
            education_required=job.education_required,
            qualifications=job.qualifications,
        )

        # Build resume keyword set from skills + candidate name tokens
        resume_keywords: list[str] = list(resume.skills)
        for exp in resume.experience:
            resume_keywords.extend(exp.skills)
        for proj in resume.projects:
            resume_keywords.extend(proj.skills)

        keyword_result = self._keyword.match(
            resume_keywords=resume_keywords,
            job_keywords=job.keywords,
        )

        gap_result = self._gap.analyze(
            skill_result=skill_result,
            experience_result=experience_result,
            education_result=education_result,
            keyword_result=keyword_result,
        )

        return self._builder.build(
            skill_result=skill_result,
            experience_result=experience_result,
            education_result=education_result,
            keyword_result=keyword_result,
            gap_result=gap_result,
        )
