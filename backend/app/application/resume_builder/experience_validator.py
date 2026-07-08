"""Validator for checking Experience fields and constraints."""

import re
from typing import Any


class ExperienceValidationError(Exception):
    """Exception raised when experience validation fails."""

    pass


class ExperienceValidator:
    """Validator for verifying Experience fields and constraints."""

    def validate(self, records: list[dict[str, Any]]) -> dict[str, list[str]]:
        """Validate mapped experience records.

        Args:
            records: List of raw mapped experience data dictionaries.

        Returns:
            A dictionary mapping field names/indices to lists of error messages.
        """
        errors: dict[str, list[str]] = {}

        if not records:
            errors.setdefault("general", []).append(
                "Experience section cannot be empty"
            )
            return errors

        seen = set()

        for idx, rec in enumerate(records):
            prefix = f"record_{idx}"
            company = rec.get("company")
            role = rec.get("role")
            start = rec.get("start_date")
            end = rec.get("end_date")
            current = rec.get("current_position")

            # 1. Required Company Name
            if not company or not str(company).strip():
                errors.setdefault(f"{prefix}.company", []).append(
                    "Company Name is required"
                )

            # 2. Required Job Title
            if not role or not str(role).strip():
                errors.setdefault(f"{prefix}.role", []).append("Job Title is required")

            # 3. Duplicate Experience Entries
            entry_key = (
                str(company).lower().strip() if company else "",
                str(role).lower().strip() if role else "",
            )
            if company and role:
                if entry_key in seen:
                    errors.setdefault(f"{prefix}.duplicate", []).append(
                        f"Duplicate experience entry: {company}, {role}"
                    )
                seen.add(entry_key)

            # 4. Date consistency
            if start and end:
                self._validate_dates(start, end, f"{prefix}.dates", errors)

            # 5. Current position logic
            if current:
                if not end or end.lower() not in ("present", "current", "now"):
                    errors.setdefault(f"{prefix}.current_position", []).append(
                        "Current position end date must be Present, Current, or Now"
                    )
            else:
                if end and end.lower() in ("present", "current", "now"):
                    errors.setdefault(f"{prefix}.current_position", []).append(
                        "Non-current position cannot have "
                        "Present, Current, or Now as end date"
                    )

        return errors

    def _validate_dates(
        self,
        start: str,
        end: str,
        key: str,
        errors: dict[str, list[str]],
    ) -> None:
        """Helper to validate start and end date consistency."""
        year_re = re.compile(r"\b(19\d{2}|2\d{3})\b")
        start_years = year_re.findall(start)
        end_years = year_re.findall(end)

        if start_years and end_years:
            start_yr = int(start_years[0])
            end_yr = int(end_years[0])
            if start_yr > end_yr:
                errors.setdefault(key, []).append(
                    f"Start year ({start_yr}) cannot be after end year ({end_yr})"
                )
        elif start_years and not end_years and not end:
            # If start year exists but end is completely empty and current is False,
            # this is acceptable, but let's check for year format only.
            pass
        elif not start_years and start:
            # Start date format validation is optional but we can verify it
            pass
