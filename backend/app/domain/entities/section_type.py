"""Domain enum representing logical section types within a document."""

from enum import StrEnum


class SectionType(StrEnum):
    """Logical categories of sections within a document."""

    SUMMARY = "summary"
    PROFILE = "profile"
    OBJECTIVE = "objective"
    EDUCATION = "education"
    EXPERIENCE = "experience"
    PROJECTS = "projects"
    SKILLS = "skills"
    CERTIFICATIONS = "certifications"
    ACHIEVEMENTS = "achievements"
    PUBLICATIONS = "publications"
    LANGUAGES = "languages"
    CONTACT = "contact"
    INTERESTS = "interests"
    VOLUNTEER = "volunteer"
    AWARDS = "awards"
    OTHER = "other"
    UNKNOWN = "unknown"
