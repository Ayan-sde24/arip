"""Validator for checking Education fields and constraints."""

import re
from typing import Any


class EducationValidationError(Exception):
    """Exception raised when education validation fails."""

    pass


class EducationValidator:
    """Validator for verifying Education fields and constraints."""

    def validate(self, records: list[dict[str, Any]]) -> dict[str, list[str]]:
        """Validate mapped education records.

        Args:
            records: List of raw mapped education data dictionaries.

        Returns:
            A dictionary mapping field names/indices to lists of error messages.
        """
        errors: dict[str, list[str]] = {}

        if not records:
            errors.setdefault("general", []).append("Education section cannot be empty")
            return errors

        seen = set()

        for idx, rec in enumerate(records):
            prefix = f"record_{idx}"
            inst = rec.get("institution")
            deg = rec.get("degree")
            major = rec.get("major")
            start = rec.get("start_date")
            end = rec.get("end_date")

            # 1. Required Institution
            if not inst or not str(inst).strip():
                errors.setdefault(f"{prefix}.institution", []).append(
                    "Institution is required"
                )

            # 2. Required Degree
            if not deg or not str(deg).strip():
                errors.setdefault(f"{prefix}.degree", []).append("Degree is required")

            # 3. Duplicate Education Entries
            # Same institution, degree, major
            entry_key = (
                str(inst).lower().strip() if inst else "",
                str(deg).lower().strip() if deg else "",
                str(major).lower().strip() if major else "",
            )
            if inst and deg:
                if entry_key in seen:
                    errors.setdefault(f"{prefix}.duplicate", []).append(
                        f"Duplicate education entry: {inst}, {deg}"
                    )
                seen.add(entry_key)

            # 4. Date consistency
            if start and end:
                self._validate_dates(start, end, f"{prefix}.dates", errors)

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
