"""Deterministic education matcher comparing resume education to job requirements."""

from __future__ import annotations

import re
from dataclasses import dataclass

from app.domain.entities.resume import Education

# Ordered degree tiers — higher index = higher level
_DEGREE_TIERS: list[list[str]] = [
    ["high school", "secondary", "diploma", "ged"],
    ["associate", "aa", "as"],
    ["bachelor", "bs", "ba", "b.s", "b.a", "btech", "b.tech", "undergraduate", "ug"],
    [
        "master",
        "ms",
        "ma",
        "m.s",
        "m.a",
        "mtech",
        "m.tech",
        "mba",
        "postgraduate",
        "pg",
    ],
    ["phd", "doctorate", "doctor", "d.phil"],
]


def _degree_tier(text: str) -> int:
    """Return the tier index of a degree string, or -1 if unknown."""
    lower = text.lower()
    for i, synonyms in enumerate(_DEGREE_TIERS):
        if any(s in lower for s in synonyms):
            return i
    return -1


def _normalise(text: str) -> str:
    return re.sub(r"[^a-z0-9 ]", "", text.lower()).strip()


@dataclass(frozen=True)
class EducationMatchResult:
    """Result of education matching."""

    required_tier: int
    highest_resume_tier: int
    degree_satisfied: bool
    major_match: bool
    education_score: float
    notes: list[str]


class EducationMatcher:
    """Compares resume education against job education requirements.

    Deterministic strategy; semantic similarity can be plugged in later
    without API changes.
    """

    def match(
        self,
        education_list: list[Education],
        education_required: str | None,
        qualifications: list[str],
    ) -> EducationMatchResult:
        """Return education match metrics.

        Args:
            education_list: Resume education records.
            education_required: Raw string like 'Bachelor in CS'.
            qualifications: Job qualifications list for major/field inference.

        Returns:
            EducationMatchResult with score and notes.
        """
        notes: list[str] = []

        # ── Degree tier comparison ────────────────────────────────────────────
        req_text = education_required or ""
        required_tier = _degree_tier(req_text)
        highest_resume_tier = max(
            (_degree_tier(f"{e.degree or ''} {e.major or ''}") for e in education_list),
            default=-1,
        )

        if required_tier == -1:
            # No explicit education requirement
            degree_satisfied = True
            degree_score = 100.0
        elif highest_resume_tier >= required_tier:
            degree_satisfied = True
            degree_score = 100.0
        else:
            degree_satisfied = False
            gap = required_tier - highest_resume_tier
            degree_score = max(0.0, 100.0 - gap * 25.0)
            notes.append(
                f"Degree tier below requirement: found tier {highest_resume_tier}, "
                f"required tier {required_tier}"
            )

        # ── Major / field-of-study relevance ─────────────────────────────────
        req_combined = _normalise(req_text + " " + " ".join(qualifications))
        major_match = False
        for edu in education_list:
            major_norm = _normalise(edu.major or "")
            degree_norm = _normalise(edu.degree or "")
            if major_norm and (
                major_norm in req_combined
                or any(
                    token in req_combined
                    for token in major_norm.split()
                    if len(token) > 3
                )
            ):
                major_match = True
                break
            if degree_norm and (
                degree_norm in req_combined
                or any(
                    token in req_combined
                    for token in degree_norm.split()
                    if len(token) > 3
                )
            ):
                major_match = True
                break

        major_score = 100.0 if major_match else 70.0
        if not major_match and education_list:
            notes.append("Major/field of study not explicitly matched")

        score = round(degree_score * 0.7 + major_score * 0.3, 2)

        return EducationMatchResult(
            required_tier=required_tier,
            highest_resume_tier=highest_resume_tier,
            degree_satisfied=degree_satisfied,
            major_match=major_match,
            education_score=score,
            notes=notes,
        )
