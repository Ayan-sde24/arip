"""Validator for checking JobDescription fields and constraints."""

from typing import Any


class JobValidationError(Exception):
    """Raised when job description validation fails."""

    pass


class JobValidator:
    """Validates mapped job description records."""

    def validate(self, record: dict[str, Any]) -> dict[str, list[str]]:
        """Validate a single mapped job description record.

        Args:
            record: Mapped raw job description data.

        Returns:
            Dict of field names to error message lists.
        """
        errors: dict[str, list[str]] = {}

        # Required: title
        title = record.get("title", "")
        if not title or not str(title).strip():
            errors.setdefault("title", []).append("Job Title is required")

        # Required: company
        company = record.get("company", "")
        if not company or not str(company).strip():
            errors.setdefault("company", []).append("Company Name is required")

        # Required: at least one required skill
        required_skills = record.get("required_skills", [])
        if not required_skills:
            errors.setdefault("required_skills", []).append(
                "At least one required skill must be present"
            )

        # Duplicate required skills
        seen: set[str] = set()
        for skill in required_skills:
            key = skill.lower().strip()
            if key in seen:
                errors.setdefault("required_skills.duplicate", []).append(
                    f"Duplicate required skill: {skill}"
                )
            seen.add(key)

        # Duplicate preferred skills
        seen_pref: set[str] = set()
        for skill in record.get("preferred_skills", []):
            key = skill.lower().strip()
            if key in seen_pref:
                errors.setdefault("preferred_skills.duplicate", []).append(
                    f"Duplicate preferred skill: {skill}"
                )
            seen_pref.add(key)

        # Empty responsibilities list is a warning-level error
        responsibilities = record.get("responsibilities", [])
        if not responsibilities:
            errors.setdefault("responsibilities", []).append(
                "Responsibilities section cannot be empty"
            )

        return errors
