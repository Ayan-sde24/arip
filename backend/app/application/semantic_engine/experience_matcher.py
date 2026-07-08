"""Deterministic experience matcher comparing resume experience to job requirements."""

from __future__ import annotations

import re
from dataclasses import dataclass

from app.domain.entities.resume import Experience


def _extract_years(text: str) -> float:
    """Parse the first number (int or float) from a years-of-experience string."""
    m = re.search(r"(\d+(?:\.\d+)?)", text or "")
    return float(m.group(1)) if m else 0.0


def _normalise(text: str) -> str:
    return re.sub(r"[^a-z0-9 ]", "", text.lower()).strip()


@dataclass(frozen=True)
class ExperienceMatchResult:
    """Result of experience matching."""

    years_on_resume: float
    years_required: float
    years_gap: float
    role_matches: list[str]
    technology_matches: list[str]
    experience_score: float
    notes: list[str]


class ExperienceMatcher:
    """Compares resume experience against job experience requirements.

    Deterministic strategy; embedding similarity can be plugged in later
    without API changes.
    """

    _YEARS_WEIGHT: float = 0.4
    _ROLE_WEIGHT: float = 0.3
    _TECH_WEIGHT: float = 0.3

    def match(
        self,
        experience_list: list[Experience],
        experience_required: str | None,
        required_skills: list[str],
        job_title: str,
    ) -> ExperienceMatchResult:
        """Return experience match metrics.

        Args:
            experience_list: Resume experience records.
            experience_required: Raw string like '3+ years' or '5 years'.
            required_skills: Job required skills used for technology overlap.
            job_title: Job title used for role relevance check.

        Returns:
            ExperienceMatchResult with score and notes.
        """
        notes: list[str] = []

        # ── Years of experience ───────────────────────────────────────────────
        years_required = _extract_years(experience_required or "")
        years_on_resume = self._total_years(experience_list)
        years_gap = max(0.0, years_required - years_on_resume)

        if years_required == 0:
            years_score = 100.0
        else:
            years_score = min(100.0, (years_on_resume / years_required) * 100)

        if years_gap > 0:
            notes.append(
                f"{years_gap:.1f} year(s) short of required {years_required:.0f}"
            )

        # ── Role relevance ────────────────────────────────────────────────────
        title_tokens = set(_normalise(job_title).split())
        role_matches: list[str] = []
        for exp in experience_list:
            role_tokens = set(_normalise(exp.role).split())
            if title_tokens & role_tokens:
                role_matches.append(exp.role)
        role_score = 100.0 if role_matches else 0.0
        if not role_matches:
            notes.append("No directly matching roles found")

        # ── Technology overlap ────────────────────────────────────────────────
        resume_tech: set[str] = set()
        for exp in experience_list:
            for sk in exp.skills:
                resume_tech.add(_normalise(sk))
        tech_matches = [s for s in required_skills if _normalise(s) in resume_tech]
        tech_score = (
            (len(tech_matches) / len(required_skills) * 100)
            if required_skills
            else 100.0
        )

        score = round(
            years_score * self._YEARS_WEIGHT
            + role_score * self._ROLE_WEIGHT
            + tech_score * self._TECH_WEIGHT,
            2,
        )

        return ExperienceMatchResult(
            years_on_resume=round(years_on_resume, 1),
            years_required=years_required,
            years_gap=round(years_gap, 1),
            role_matches=role_matches,
            technology_matches=tech_matches,
            experience_score=score,
            notes=notes,
        )

    # ── helpers ───────────────────────────────────────────────────────────────

    @staticmethod
    def _total_years(experience_list: list[Experience]) -> float:
        """Estimate total years of experience from start/end date strings."""
        total = 0.0
        for exp in experience_list:
            start = _extract_years(exp.start_date or "")
            end_raw = exp.end_date or ""
            if "present" in end_raw.lower() or "current" in end_raw.lower():
                import datetime

                end = float(datetime.date.today().year)
            else:
                end = _extract_years(end_raw)
            if start and end and end >= start:
                total += end - start
        return total
