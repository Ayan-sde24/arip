"""Domain entities representing resume optimization reports and representations."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class OptimizedResume:
    """Optimized representation of the candidate resume."""

    summary: str
    bullet_points: list[str] = field(default_factory=list)
    suggested_skills: list[str] = field(default_factory=list)
    suggested_keywords: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ResumeOptimizationReport:
    """Core domain business entity representing the resume optimization suggestions."""

    optimization_score: float
    priority_fixes: list[str] = field(default_factory=list)
    critical_issues: list[str] = field(default_factory=list)
    suggested_improvements: list[str] = field(default_factory=list)
    optimized_resume: OptimizedResume = field(
        default_factory=lambda: OptimizedResume(summary="", bullet_points=[])
    )
