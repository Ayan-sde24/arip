"""DTO representing consolidated analysis responses for the frontend."""

from dataclasses import dataclass, field

from app.application.dto.chart_response import ChartResponseDTO
from app.application.dto.recommendation_response import RecommendationResponseDTO
from app.application.dto.score_response import ScoreResponseDTO
from app.application.dto.summary_response import SummaryResponseDTO


@dataclass(frozen=True)
class AnalysisResponseDTO:
    """Frontend-ready consolidated analysis report payload."""

    summary: SummaryResponseDTO | None
    scores: ScoreResponseDTO | None
    recommendations: RecommendationResponseDTO | None
    charts: ChartResponseDTO | None
    status: str
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
