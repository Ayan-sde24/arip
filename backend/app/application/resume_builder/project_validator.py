"""Validator for checking Project fields and constraints."""

import re
from typing import Any


class ProjectValidationError(Exception):
    """Exception raised when project validation fails."""

    pass


class ProjectValidator:
    """Validator for verifying Project fields and constraints."""

    URL_REGEX = re.compile(r"^(https?://)?(www\.)?[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")

    def validate(self, records: list[dict[str, Any]]) -> dict[str, list[str]]:
        """Validate mapped project records.

        Args:
            records: List of raw mapped project data dictionaries.

        Returns:
            A dictionary mapping field names/indices to lists of error messages.
        """
        errors: dict[str, list[str]] = {}

        if not records:
            errors.setdefault("general", []).append("Projects section cannot be empty")
            return errors

        seen = set()

        for idx, rec in enumerate(records):
            prefix = f"record_{idx}"
            title = rec.get("title")
            desc = rec.get("description")
            url = rec.get("url")

            # 1. Required Title
            if not title or not str(title).strip():
                errors.setdefault(f"{prefix}.title", []).append(
                    "Project Title is required"
                )

            # 2. Required Description
            if not desc or not str(desc).strip():
                errors.setdefault(f"{prefix}.description", []).append(
                    "Project Description is required"
                )

            # 3. Duplicate Projects
            if title:
                title_key = str(title).lower().strip()
                if title_key in seen:
                    errors.setdefault(f"{prefix}.duplicate", []).append(
                        f"Duplicate project title detected: {title}"
                    )
                seen.add(title_key)

            # 4. URL Validation
            if url:
                url_str = str(url).strip()
                if not self.URL_REGEX.match(url_str):
                    errors.setdefault(f"{prefix}.url", []).append(
                        f"Invalid URL format for project: {url}"
                    )

        return errors
