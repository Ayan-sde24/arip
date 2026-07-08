"""Mapper for extracting and parsing a job description from the CIR."""

import re
from typing import Any

from app.domain.entities.canonical_intermediate_representation import (
    CanonicalIntermediateRepresentation,
)
from app.domain.entities.section_type import SectionType

# Heuristic keyword sets used when explicit section types are absent
_TITLE_KEYWORDS = frozenset(
    [
        "job title",
        "position",
        "role",
        "opening",
        "vacancy",
    ]
)
_COMPANY_KEYWORDS = frozenset(["company", "organization", "employer", "about us"])
_LOCATION_KEYWORDS = frozenset(["location", "city", "office", "remote", "hybrid"])
_EMP_TYPE_KEYWORDS = frozenset(
    ["employment type", "job type", "contract type", "work type"]
)
_EXP_KEYWORDS = frozenset(
    ["experience required", "years of experience", "experience", "exp"]
)
_EDU_KEYWORDS = frozenset(
    ["education required", "educational requirement", "qualification", "degree"]
)
_RESP_KEYWORDS = frozenset(
    ["responsibilities", "what you'll do", "duties", "role overview", "your role"]
)
_QUAL_KEYWORDS = frozenset(
    [
        "qualifications",
        "requirements",
        "what we're looking for",
        "what you bring",
    ]
)
_REQ_SKILLS_KEYWORDS = frozenset(
    ["required skills", "must have", "technical skills", "core skills"]
)
_PREF_SKILLS_KEYWORDS = frozenset(
    ["preferred skills", "nice to have", "bonus skills", "additional skills"]
)
_BENEFITS_KEYWORDS = frozenset(["benefits", "perks", "what we offer", "compensation"])
_SALARY_KEYWORDS = frozenset(["salary", "pay", "compensation range", "ctc"])
_KEYWORDS_KEYWORDS = frozenset(["keywords", "tags", "skills", "technologies"])


def _section_text(cir: CanonicalIntermediateRepresentation, *types: SectionType) -> str:
    """Return concatenated content of all sections matching any of the given types."""
    parts = [sec.content for sec in cir.sections if sec.section_type in types]
    return "\n".join(parts).strip()


def _bullet_lines(text: str) -> list[str]:
    """Split text into cleaned non-empty lines, stripping bullet markers."""
    lines = []
    for line in text.splitlines():
        clean = re.sub(r"^[\s\-\*•·\d\.]+", "", line).strip()
        if clean:
            lines.append(clean)
    return lines


def _csv_skills(text: str) -> list[str]:
    """Split comma/semicolon separated skill strings and return cleaned list."""
    parts = re.split(r"[,;]", text)
    return [p.strip() for p in parts if p.strip()]


def _find_section_by_keywords(
    cir: CanonicalIntermediateRepresentation,
    keywords: frozenset[str],
) -> str:
    """Fallback: find section whose title matches any keyword heuristic."""
    for sec in cir.sections:
        title_lower = (sec.title or "").lower()
        content_first_line = sec.content.splitlines()[0].lower() if sec.content else ""
        for kw in keywords:
            if kw in title_lower or kw in content_first_line:
                return sec.content
    return ""


def _extract_inline_value(text: str, keywords: frozenset[str]) -> str:
    """Extract a value from lines like 'Key: Value' within raw text."""
    for line in text.splitlines():
        lower = line.lower()
        for kw in keywords:
            if lower.startswith(kw):
                parts = line.split(":", 1)
                if len(parts) == 2:
                    return parts[1].strip()
    return ""


class JobMapper:
    """Parses a CIR into a raw job description record dict."""

    def map_cir_to_job_record(
        self,
        cir: CanonicalIntermediateRepresentation,
    ) -> dict[str, Any]:
        """Extract all JD fields from the CIR.

        Strategy:
        1. Use explicit SectionType values when available.
        2. Fall back to keyword heuristics on section titles / first lines.
        3. Fall back to inline 'Key: Value' scanning of the full raw text.
        """
        full_text = cir.document_content.raw_text or ""

        # ── Title ─────────────────────────────────────────────────────────────
        title = (
            _section_text(cir, SectionType.JOB_TITLE).splitlines()[0].strip()
            if _section_text(cir, SectionType.JOB_TITLE)
            else ""
        )
        if not title:
            title = _find_section_by_keywords(cir, _TITLE_KEYWORDS)
            title = title.splitlines()[0].strip() if title else ""
        if not title:
            title = _extract_inline_value(full_text, _TITLE_KEYWORDS)

        # ── Company ───────────────────────────────────────────────────────────
        company = (
            _section_text(cir, SectionType.COMPANY).splitlines()[0].strip()
            if _section_text(cir, SectionType.COMPANY)
            else ""
        )
        if not company:
            company = _find_section_by_keywords(cir, _COMPANY_KEYWORDS)
            company = company.splitlines()[0].strip() if company else ""
        if not company:
            company = _extract_inline_value(full_text, _COMPANY_KEYWORDS)

        # ── Location ──────────────────────────────────────────────────────────
        location_text = _section_text(cir, SectionType.LOCATION)
        location: str | None = (
            location_text.splitlines()[0].strip() if location_text else None
        )
        if not location:
            raw = _find_section_by_keywords(cir, _LOCATION_KEYWORDS)
            val = raw.splitlines()[0].strip() if raw else ""
            location = val or (
                _extract_inline_value(full_text, _LOCATION_KEYWORDS) or None
            )

        # ── Employment Type ───────────────────────────────────────────────────
        emp_text = _section_text(cir, SectionType.EMPLOYMENT_TYPE)
        employment_type: str | None = (
            emp_text.splitlines()[0].strip() if emp_text else None
        )
        if not employment_type:
            raw = _find_section_by_keywords(cir, _EMP_TYPE_KEYWORDS)
            val = raw.splitlines()[0].strip() if raw else ""
            employment_type = val or (
                _extract_inline_value(full_text, _EMP_TYPE_KEYWORDS) or None
            )

        # ── Experience Required ───────────────────────────────────────────────
        exp_text = _section_text(cir, SectionType.EXPERIENCE_REQUIRED)
        experience_required: str | None = (
            exp_text.splitlines()[0].strip() if exp_text else None
        )
        if not experience_required:
            val = _extract_inline_value(full_text, _EXP_KEYWORDS)
            experience_required = val or None

        # ── Education Required ────────────────────────────────────────────────
        edu_text = _section_text(cir, SectionType.EDUCATION_REQUIRED)
        education_required: str | None = (
            edu_text.splitlines()[0].strip() if edu_text else None
        )
        if not education_required:
            val = _extract_inline_value(full_text, _EDU_KEYWORDS)
            education_required = val or None

        # ── Required Skills ───────────────────────────────────────────────────
        req_text = _section_text(cir, SectionType.REQUIRED_SKILLS)
        if req_text:
            required_skills = _csv_skills(req_text) or _bullet_lines(req_text)
        else:
            raw = _find_section_by_keywords(cir, _REQ_SKILLS_KEYWORDS)
            required_skills = _csv_skills(raw) if raw else []

        # ── Preferred Skills ──────────────────────────────────────────────────
        pref_text = _section_text(cir, SectionType.PREFERRED_SKILLS)
        if pref_text:
            preferred_skills = _csv_skills(pref_text) or _bullet_lines(pref_text)
        else:
            raw = _find_section_by_keywords(cir, _PREF_SKILLS_KEYWORDS)
            preferred_skills = _csv_skills(raw) if raw else []

        # ── Responsibilities ──────────────────────────────────────────────────
        resp_text = _section_text(cir, SectionType.RESPONSIBILITIES)
        if not resp_text:
            resp_text = _find_section_by_keywords(cir, _RESP_KEYWORDS)
        responsibilities = _bullet_lines(resp_text)

        # ── Qualifications ────────────────────────────────────────────────────
        qual_text = _section_text(cir, SectionType.QUALIFICATIONS)
        if not qual_text:
            qual_text = _find_section_by_keywords(cir, _QUAL_KEYWORDS)
        qualifications = _bullet_lines(qual_text)

        # ── Benefits ──────────────────────────────────────────────────────────
        ben_text = _section_text(cir, SectionType.BENEFITS)
        if not ben_text:
            ben_text = _find_section_by_keywords(cir, _BENEFITS_KEYWORDS)
        benefits = _bullet_lines(ben_text)

        # ── Salary ────────────────────────────────────────────────────────────
        sal_text = _section_text(cir, SectionType.SALARY)
        salary: str | None = sal_text.splitlines()[0].strip() if sal_text else None
        if not salary:
            val = _extract_inline_value(full_text, _SALARY_KEYWORDS)
            salary = val or None

        # ── Keywords ──────────────────────────────────────────────────────────
        kw_text = _section_text(cir, SectionType.KEYWORDS)
        if kw_text:
            keywords = _csv_skills(kw_text) or _bullet_lines(kw_text)
        else:
            # Derive from union of required + preferred skill names
            keywords = list(
                dict.fromkeys(
                    [s.lower() for s in required_skills]
                    + [s.lower() for s in preferred_skills]
                )
            )

        return {
            "title": title,
            "company": company,
            "location": location,
            "employment_type": employment_type,
            "experience_required": experience_required,
            "education_required": education_required,
            "required_skills": required_skills,
            "preferred_skills": preferred_skills,
            "responsibilities": responsibilities,
            "qualifications": qualifications,
            "benefits": benefits,
            "salary": salary,
            "keywords": keywords,
        }
