"""Domain entity representing a candidate in the system."""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class Candidate:
    """Core domain business entity representing a candidate/applicant."""

    candidate_id: UUID
    name: str
    email: str
    phone: str
    linkedin: str | None = None
    github: str | None = None
    portfolio: str | None = None
    location: str | None = None
