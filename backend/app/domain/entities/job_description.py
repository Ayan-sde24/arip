"""Domain entity representing a job description."""

from dataclasses import dataclass, field

from app.domain.entities.document import Document


@dataclass(frozen=True)
class JobDescription:
    """Core domain business entity representing a job description target."""

    document: Document
    company: str
    title: str
    requirements: list[str] = field(default_factory=list)
    responsibilities: list[str] = field(default_factory=list)
    preferred_skills: list[str] = field(default_factory=list)
