"""Domain entity representing a job description."""

from dataclasses import dataclass, field

from app.domain.entities.document import Document


@dataclass(frozen=True)
class JobDescription:
    """Core domain business entity representing a parsed job description."""

    document: Document
    title: str
    company: str
    location: str | None = None
    employment_type: str | None = None
    experience_required: str | None = None
    education_required: str | None = None
    required_skills: list[str] = field(default_factory=list)
    preferred_skills: list[str] = field(default_factory=list)
    responsibilities: list[str] = field(default_factory=list)
    qualifications: list[str] = field(default_factory=list)
    benefits: list[str] = field(default_factory=list)
    salary: str | None = None
    keywords: list[str] = field(default_factory=list)
    # legacy alias kept for backwards compat
    requirements: list[str] = field(default_factory=list)
