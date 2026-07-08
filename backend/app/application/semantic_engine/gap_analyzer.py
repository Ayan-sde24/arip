"""Gap analyzer: synthesises match results into gap and strength areas."""

from __future__ import annotations

from dataclasses import dataclass

from app.application.semantic_engine.education_matcher import EducationMatchResult
from app.application.semantic_engine.experience_matcher import ExperienceMatchResult
from app.application.semantic_engine.keyword_matcher import KeywordMatchResult
from app.application.semantic_engine.skill_matcher import SkillMatchResult
from app.domain.entities.semantic_match_report import GapSummary

# Score thresholds
_WEAK_THRESHOLD = 60.0
_STRENGTH_THRESHOLD = 85.0


@dataclass(frozen=True)
class GapAnalysisResult:
    """Internal result passed to report builder."""

    gap_summary: GapSummary
    recommendations: list[str]


class GapAnalyzer:
    """Produces a GapSummary and recommendations from individual match results."""

    def analyze(
        self,
        skill_result: SkillMatchResult,
        experience_result: ExperienceMatchResult,
        education_result: EducationMatchResult,
        keyword_result: KeywordMatchResult,
    ) -> GapAnalysisResult:
        """Generate gap and strength areas from all match component results.

        Args:
            skill_result: Output of SkillMatcher.
            experience_result: Output of ExperienceMatcher.
            education_result: Output of EducationMatcher.
            keyword_result: Output of KeywordMatcher.

        Returns:
            GapAnalysisResult with structured gap summary and recommendations.
        """
        missing_skills = skill_result.missing_required
        missing_experience: list[str] = []
        missing_education: list[str] = []
        weak_areas: list[str] = []
        strength_areas: list[str] = []
        recommendations: list[str] = []

        # ── Skills ────────────────────────────────────────────────────────────
        if skill_result.skill_score >= _STRENGTH_THRESHOLD:
            strength_areas.append("Skills")
        elif skill_result.skill_score < _WEAK_THRESHOLD:
            weak_areas.append("Skills")
        if missing_skills:
            recommendations.append(
                f"Acquire missing required skills: {', '.join(missing_skills[:5])}"
            )

        # ── Experience ────────────────────────────────────────────────────────
        if experience_result.years_gap > 0:
            missing_experience.append(
                f"{experience_result.years_gap:.1f} more year(s) of relevant experience"
            )
            recommendations.append(
                f"Gain {experience_result.years_gap:.1f} more year(s) of experience"
            )
        if not experience_result.role_matches:
            missing_experience.append("No directly matching roles detected")
            recommendations.append(
                "Highlight roles more closely aligned with the job title"
            )
        if experience_result.experience_score >= _STRENGTH_THRESHOLD:
            strength_areas.append("Experience")
        elif experience_result.experience_score < _WEAK_THRESHOLD:
            weak_areas.append("Experience")

        # ── Education ─────────────────────────────────────────────────────────
        if not education_result.degree_satisfied:
            missing_education.append("Degree requirement not met")
            recommendations.append(
                "Consider pursuing or highlighting equivalent qualifications"
            )
        if not education_result.major_match:
            missing_education.append("Field of study not directly relevant")
        if education_result.education_score >= _STRENGTH_THRESHOLD:
            strength_areas.append("Education")
        elif education_result.education_score < _WEAK_THRESHOLD:
            weak_areas.append("Education")

        # ── Keywords ──────────────────────────────────────────────────────────
        if keyword_result.keyword_score >= _STRENGTH_THRESHOLD:
            strength_areas.append("Keywords")
        elif keyword_result.keyword_score < _WEAK_THRESHOLD:
            weak_areas.append("Keywords")
            if keyword_result.missing_keywords:
                recommendations.append(
                    f"Incorporate missing keywords: "
                    f"{', '.join(keyword_result.missing_keywords[:5])}"
                )

        return GapAnalysisResult(
            gap_summary=GapSummary(
                missing_skills=missing_skills,
                missing_experience=missing_experience,
                missing_education=missing_education,
                weak_areas=weak_areas,
                strength_areas=strength_areas,
            ),
            recommendations=recommendations,
        )
