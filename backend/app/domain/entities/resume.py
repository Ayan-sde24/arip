"""Domain entities representing resume details and collections."""

from dataclasses import dataclass, field

from app.domain.entities.candidate import Candidate
from app.domain.entities.document import Document


@dataclass(frozen=True)
class Education:
    """Represents an education record parsed from a resume."""

    institution: str
    degree: str | None = None
    major: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    gpa: float | None = None
    details: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class Experience:
    """Represents a work experience record parsed from a resume."""

    company: str
    role: str
    location: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    description: list[str] = field(default_factory=list)
    skills: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class Project:
    """Represents a personal or professional project record parsed from a resume."""

    title: str
    description: str | None = None
    url: str | None = None
    skills: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class Certification:
    """Represents a professional certification record parsed from a resume."""

    name: str
    issuer: str | None = None
    issue_date: str | None = None
    expiration_date: str | None = None
    url: str | None = None


@dataclass(frozen=True)
class Achievement:
    """Represents an award, honor, or milestone parsed from a resume."""

    title: str
    description: str | None = None
    date: str | None = None


@dataclass(frozen=True)
class Resume:
    """Domain business entity representing a candidate resume."""

    document: Document
    candidate: Candidate | None = None
    education: list[Education] = field(default_factory=list)
    experience: list[Experience] = field(default_factory=list)
    projects: list[Project] = field(default_factory=list)
    skills: list[str] = field(default_factory=list)
    certifications: list[Certification] = field(default_factory=list)
    achievements: list[Achievement] = field(default_factory=list)
