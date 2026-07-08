"""Validator for checking Achievement fields and constraints."""

from typing import Any


class AchievementValidationError(Exception):
    """Exception raised when achievement validation fails."""

    pass


class AchievementValidator:
    """Validator for verifying Achievement fields and constraints."""

    def validate(self, records: list[dict[str, Any]]) -> dict[str, list[str]]:
        """Validate mapped achievement records.

        Args:
            records: List of raw mapped achievement data dictionaries.

        Returns:
            A dictionary mapping field names/indices to lists of error messages.
        """
        errors: dict[str, list[str]] = {}

        if not records:
            errors.setdefault("general", []).append(
                "Achievements section cannot be empty"
            )
            return errors

        seen = set()

        for idx, rec in enumerate(records):
            prefix = f"record_{idx}"
            title = rec.get("title")
            desc = rec.get("description")

            # 1. Required Title
            if not title or not str(title).strip():
                errors.setdefault(f"{prefix}.title", []).append(
                    "Achievement Title is required"
                )

            # 2. Required Description
            if not desc or not str(desc).strip():
                errors.setdefault(f"{prefix}.description", []).append(
                    "Achievement Description is required"
                )

            # 3. Duplicate Achievements
            if title:
                title_key = str(title).lower().strip()
                if title_key in seen:
                    errors.setdefault(f"{prefix}.duplicate", []).append(
                        f"Duplicate achievement detected: {title}"
                    )
                seen.add(title_key)

        return errors
