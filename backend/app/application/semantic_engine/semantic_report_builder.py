"""Assembles all matcher results and gap analysis into a SemanticMatchReport."""

from __future__ import annotations

from app.application.semantic_engine.education_matcher import EducationMatchResult
from app.application.semantic_engine.experience_matcher import ExperienceMatchResult
from app.application.semantic_engine.gap_analyzer import GapAnalysisResult
from app.application.semantic_engine.keyword_matcher import KeywordMatchResult
from app.application.semantic_engine.skill_matcher import SkillMatchResult
from app.domain.entities.semantic_match_report import MatchEvidence, SemanticMatchReport

# Component weights for overall score
_SKILL_WEIGHT = 0.40
_EXPERIENCE_WEIGHT = 0.30
_EDUCATION_WEIGHT = 0.15
_KEYWORD_WEIGHT = 0.15


class SemanticReportBuilder:
    """Constructs the final SemanticMatchReport from all component results."""

    def build(
        self,
        skill_result: SkillMatchResult,
        experience_result: ExperienceMatchResult,
        education_result: EducationMatchResult,
        keyword_result: KeywordMatchResult,
        gap_result: GapAnalysisResult,
    ) -> SemanticMatchReport:
        """Assemble and return a SemanticMatchReport.

        Args:
            skill_result: Output of SkillMatcher.
            experience_result: Output of ExperienceMatcher.
            education_result: Output of EducationMatcher.
            keyword_result: Output of KeywordMatcher.
            gap_result: Output of GapAnalyzer.

        Returns:
            Fully populated SemanticMatchReport.
        """
        overall = round(
            skill_result.skill_score * _SKILL_WEIGHT
            + experience_result.experience_score * _EXPERIENCE_WEIGHT
            + education_result.education_score * _EDUCATION_WEIGHT
            + keyword_result.keyword_score * _KEYWORD_WEIGHT,
            2,
        )

        evidence = self._build_evidence(
            skill_result, experience_result, education_result, keyword_result
        )

        return SemanticMatchReport(
            overall_score=overall,
            skill_score=skill_result.skill_score,
            experience_score=experience_result.experience_score,
            education_score=education_result.education_score,
            keyword_score=keyword_result.keyword_score,
            matched_skills=skill_result.matched_required,
            missing_skills=skill_result.missing_required,
            extra_skills=skill_result.extra_skills,
            matched_preferred_skills=skill_result.matched_preferred,
            required_skill_coverage=skill_result.required_coverage,
            preferred_skill_coverage=skill_result.preferred_coverage,
            matched_keywords=keyword_result.matched_keywords,
            missing_keywords=keyword_result.missing_keywords,
            keyword_coverage=keyword_result.keyword_coverage,
            gap_summary=gap_result.gap_summary,
            evidence=evidence,
            recommendations=gap_result.recommendations,
        )

    # ── private ───────────────────────────────────────────────────────────────

    @staticmethod
    def _build_evidence(
        skill: SkillMatchResult,
        experience: ExperienceMatchResult,
        education: EducationMatchResult,
        keyword: KeywordMatchResult,
    ) -> list[MatchEvidence]:
        evidence: list[MatchEvidence] = []

        # Skills
        total_req = len(skill.matched_required) + len(skill.missing_required)
        evidence.append(
            MatchEvidence(
                component="Skills",
                reason=(
                    f"Matched {len(skill.matched_required)} of {total_req} "
                    f"required skills ({skill.required_coverage:.0f}% coverage)"
                ),
            )
        )

        # Experience
        if experience.years_gap > 0:
            exp_reason = (
                f"{experience.years_gap:.1f} year(s) short of required "
                f"{experience.years_required:.0f}"
            )
        else:
            exp_reason = (
                f"Experience requirement met "
                f"({experience.years_on_resume:.1f} years on resume)"
            )
        if experience.notes:
            exp_reason += f"; {experience.notes[0]}"
        evidence.append(MatchEvidence(component="Experience", reason=exp_reason))

        # Education
        if education.degree_satisfied:
            edu_reason = "Degree requirement satisfied"
        else:
            edu_reason = (
                f"Degree requirement not met "
                f"(required tier {education.required_tier}, "
                f"found tier {education.highest_resume_tier})"
            )
        evidence.append(MatchEvidence(component="Education", reason=edu_reason))

        # Keywords
        evidence.append(
            MatchEvidence(
                component="Keywords",
                reason=(
                    f"Matched {len(keyword.matched_keywords)} of "
                    f"{len(keyword.matched_keywords) + len(keyword.missing_keywords)} "
                    f"keywords ({keyword.keyword_coverage:.0f}% coverage)"
                ),
            )
        )

        return evidence
