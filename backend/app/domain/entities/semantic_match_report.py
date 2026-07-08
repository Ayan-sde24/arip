"""Domain entity representing the result of a semantic resume-to-job match."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class MatchEvidence:
    """Structured evidence entry explaining a component's contribution to the score."""

    component: str
    reason: str


@dataclass(frozen=True)
class GapSummary:
    """Structured gap analysis result."""

    missing_skills: list[str] = field(default_factory=list)
    missing_experience: list[str] = field(default_factory=list)
    missing_education: list[str] = field(default_factory=list)
    weak_areas: list[str] = field(default_factory=list)
    strength_areas: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class SemanticMatchReport:
    """Full semantic match report produced by the Semantic Intelligence Engine."""

    overall_score: float
    skill_score: float
    experience_score: float
    education_score: float
    keyword_score: float
    matched_skills: list[str] = field(default_factory=list)
    missing_skills: list[str] = field(default_factory=list)
    extra_skills: list[str] = field(default_factory=list)
    matched_preferred_skills: list[str] = field(default_factory=list)
    required_skill_coverage: float = 0.0
    preferred_skill_coverage: float = 0.0
    matched_keywords: list[str] = field(default_factory=list)
    missing_keywords: list[str] = field(default_factory=list)
    keyword_coverage: float = 0.0
    gap_summary: GapSummary = field(default_factory=GapSummary)
    evidence: list[MatchEvidence] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
