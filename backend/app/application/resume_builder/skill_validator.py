"""Validator for checking Skill fields and constraints."""

from typing import Any


class SkillValidationError(Exception):
    """Exception raised when skill validation fails."""

    pass


class SkillValidator:
    """Validator for verifying Skill fields and constraints."""

    def validate(self, records: list[dict[str, Any]]) -> dict[str, list[str]]:
        """Validate mapped skill records.

        Args:
            records: List of raw mapped skill data dictionaries.

        Returns:
            A dictionary mapping field names/indices to lists of error messages.
        """
        errors: dict[str, list[str]] = {}

        if not records:
            errors.setdefault("general", []).append("Skills section cannot be empty")
            return errors

        seen = set()

        for idx, rec in enumerate(records):
            prefix = f"record_{idx}"
            name = rec.get("name")

            # 1. Required Name
            if not name or not str(name).strip():
                errors.setdefault(f"{prefix}.name", []).append("Skill Name is required")

            # 2. Duplicate Skill Name
            if name:
                name_key = str(name).lower().strip()
                if name_key in seen:
                    errors.setdefault(f"{prefix}.duplicate", []).append(
                        f"Duplicate skill name detected: {name}"
                    )
                seen.add(name_key)

        return errors
