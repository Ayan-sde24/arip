"""Deterministic keyword matcher comparing resume keywords to job keywords."""

from __future__ import annotations

import re
from dataclasses import dataclass


def _normalise(text: str) -> str:
    return re.sub(r"[^a-z0-9 ]", "", text.lower()).strip()


def _extract_tokens(texts: list[str]) -> set[str]:
    """Tokenise a list of strings into a normalised word set."""
    tokens: set[str] = set()
    for t in texts:
        for word in _normalise(t).split():
            if len(word) > 2:
                tokens.add(word)
    return tokens


@dataclass(frozen=True)
class KeywordMatchResult:
    """Result of keyword matching."""

    matched_keywords: list[str]
    missing_keywords: list[str]
    keyword_coverage: float
    keyword_score: float


class KeywordMatcher:
    """Compares resume content tokens against job keywords.

    Deterministic token-based strategy; embedding-based similarity
    can be substituted later without API changes.
    """

    def match(
        self,
        resume_keywords: list[str],
        job_keywords: list[str],
    ) -> KeywordMatchResult:
        """Return keyword match metrics.

        Args:
            resume_keywords: Keywords/terms extracted from the resume.
            job_keywords: Keywords/terms from the job description.

        Returns:
            KeywordMatchResult with coverage % and matched/missing lists.
        """
        if not job_keywords:
            return KeywordMatchResult(
                matched_keywords=[],
                missing_keywords=[],
                keyword_coverage=100.0,
                keyword_score=100.0,
            )

        resume_tokens = _extract_tokens(resume_keywords)
        job_norm = {_normalise(kw): kw for kw in job_keywords if kw.strip()}

        matched = [orig for norm, orig in job_norm.items() if norm in resume_tokens]
        missing = [orig for norm, orig in job_norm.items() if norm not in resume_tokens]

        coverage = round((len(matched) / len(job_norm)) * 100, 2) if job_norm else 100.0
        score = coverage  # 1-to-1 for keyword layer

        return KeywordMatchResult(
            matched_keywords=matched,
            missing_keywords=missing,
            keyword_coverage=coverage,
            keyword_score=round(score, 2),
        )
