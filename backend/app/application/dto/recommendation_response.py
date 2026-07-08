"""DTO representing recommendations and improvements for the frontend."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class RecommendationResponseDTO:
    """Feedback recommendations including strengths, weaknesses, and key actions."""

    strengths: list[str] = field(default_factory=list)
    weaknesses: list[str] = field(default_factory=list)
    critical_improvements: list[str] = field(default_factory=list)
    suggested_skills: list[str] = field(default_factory=list)
    missing_keywords: list[str] = field(default_factory=list)
    career_suggestions: list[str] = field(default_factory=list)
