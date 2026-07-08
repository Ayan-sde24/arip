"""DTO representing summary-level analysis details for the frontend."""

from dataclasses import dataclass


@dataclass(frozen=True)
class SummaryResponseDTO:
    """Summary of overall analysis, candidate, scores, and general verdict."""

    candidate_name: str
    overall_match: float
    ats_score: float
    recruiter_score: float
    semantic_score: float
    optimization_score: float
    overall_recommendation: str
