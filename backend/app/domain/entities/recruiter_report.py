"""Domain entity representing the recruiter intelligence report."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class RecruiterReport:
    """Core domain business entity representing the recruiter evaluation report."""

    overall_recruiter_score: float
    project_score: float
    experience_score: float
    presentation_score: float
    leadership_score: float
    communication_score: float
    shortlist_probability: str  # "High", "Medium", "Low"
    recruiter_verdict: str  # "Strong Buy", "Buy", "Hold", "Pass"
    reasons: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    strengths: list[str] = field(default_factory=list)
    weaknesses: list[str] = field(default_factory=list)
    key_concerns: list[str] = field(default_factory=list)
    standout_factors: list[str] = field(default_factory=list)
    improvement_suggestions: list[str] = field(default_factory=list)
