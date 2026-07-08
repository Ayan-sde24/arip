"""DTO representing score details for the frontend."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ScoreResponseDTO:
    """Breakdown of scores computed by different pipeline layers."""

    ats: float
    semantic: float
    recruiter: float
    resume_quality: float
    overall: float
