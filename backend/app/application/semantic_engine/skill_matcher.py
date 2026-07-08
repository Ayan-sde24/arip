"""Deterministic skill matcher: resume skills vs job required/preferred skills."""

from __future__ import annotations

import re
from dataclasses import dataclass


def _normalise(skill: str) -> str:
    """Lowercase, collapse whitespace, strip punctuation for comparison."""
    return re.sub(r"[^a-z0-9 ]", "", skill.lower()).strip()


@dataclass(frozen=True)
class SkillMatchResult:
    """Result of skill matching."""

    matched_required: list[str]
    missing_required: list[str]
    matched_preferred: list[str]
    missing_preferred: list[str]
    extra_skills: list[str]
    required_coverage: float
    preferred_coverage: float
    skill_score: float


class SkillMatcher:
    """Compares resume skills against job required and preferred skills.

    The matching strategy is deterministic (exact normalised match).
    Embedding-based similarity can be injected via a subclass or decorator
    without changing this interface.
    """

    # Weights for the composite skill score
    _REQUIRED_WEIGHT: float = 0.8
    _PREFERRED_WEIGHT: float = 0.2

    def match(
        self,
        resume_skills: list[str],
        required_skills: list[str],
        preferred_skills: list[str],
    ) -> SkillMatchResult:
        """Return skill match metrics.

        Args:
            resume_skills: Normalised skills from the resume.
            required_skills: Skills the job mandates.
            preferred_skills: Skills the job prefers.

        Returns:
            SkillMatchResult with coverage %, matched/missing lists, and score.
        """
        resume_norm = {_normalise(s): s for s in resume_skills if s.strip()}
        req_norm = [_normalise(s) for s in required_skills if s.strip()]
        pref_norm = [_normalise(s) for s in preferred_skills if s.strip()]

        matched_req = [resume_norm[n] for n in req_norm if n in resume_norm]
        missing_req = [
            required_skills[i] for i, n in enumerate(req_norm) if n not in resume_norm
        ]
        matched_pref = [resume_norm[n] for n in pref_norm if n in resume_norm]
        missing_pref = [
            preferred_skills[i] for i, n in enumerate(pref_norm) if n not in resume_norm
        ]

        all_job_norm = set(req_norm) | set(pref_norm)
        extra = [s for n, s in resume_norm.items() if n not in all_job_norm]

        req_cov = (len(matched_req) / len(req_norm) * 100) if req_norm else 100.0
        pref_cov = (len(matched_pref) / len(pref_norm) * 100) if pref_norm else 100.0

        score = round(
            req_cov * self._REQUIRED_WEIGHT + pref_cov * self._PREFERRED_WEIGHT, 2
        )

        return SkillMatchResult(
            matched_required=matched_req,
            missing_required=missing_req,
            matched_preferred=matched_pref,
            missing_preferred=missing_pref,
            extra_skills=extra,
            required_coverage=round(req_cov, 2),
            preferred_coverage=round(pref_cov, 2),
            skill_score=score,
        )
