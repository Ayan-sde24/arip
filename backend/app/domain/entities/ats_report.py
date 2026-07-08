"""Domain entity representing the ATS intelligence check report."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ATSReport:
    """Core domain business entity representing the ATS compatibility report."""

    overall_ats_score: float
    keyword_score: float
    format_score: float
    section_score: float
    completeness_score: float
    resume_parseability: str  # "High", "Medium", "Low"
    ats_shortlisting_probability: str  # "High", "Medium", "Low"
    strengths: list[str] = field(default_factory=list)
    weaknesses: list[str] = field(default_factory=list)
    missing_keywords: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
