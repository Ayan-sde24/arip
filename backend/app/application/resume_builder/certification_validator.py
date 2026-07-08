"""Validator for checking Certification fields and constraints."""

import re
from typing import Any


class CertificationValidationError(Exception):
    """Exception raised when certification validation fails."""

    pass


class CertificationValidator:
    """Validator for verifying Certification fields and constraints."""

    URL_REGEX = re.compile(r"^(https?://)?(www\.)?[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")

    def validate(self, records: list[dict[str, Any]]) -> dict[str, list[str]]:
        """Validate mapped certification records.

        Args:
            records: List of raw mapped certification data dictionaries.

        Returns:
            A dictionary mapping field names/indices to lists of error messages.
        """
        errors: dict[str, list[str]] = {}

        if not records:
            errors.setdefault("general", []).append(
                "Certifications section cannot be empty"
            )
            return errors

        seen = set()

        for idx, rec in enumerate(records):
            prefix = f"record_{idx}"
            name = rec.get("name")
            url = rec.get("url")
            issue = rec.get("issue_date")
            expiry = rec.get("expiration_date")

            # 1. Required Name
            if not name or not str(name).strip():
                errors.setdefault(f"{prefix}.name", []).append(
                    "Certification Name is required"
                )

            # 2. Duplicate Certifications
            if name:
                name_key = str(name).lower().strip()
                if name_key in seen:
                    errors.setdefault(f"{prefix}.duplicate", []).append(
                        f"Duplicate certification detected: {name}"
                    )
                seen.add(name_key)

            # 3. URL Validation
            if url:
                url_str = str(url).strip()
                if not self.URL_REGEX.match(url_str):
                    errors.setdefault(f"{prefix}.url", []).append(
                        f"Invalid URL format for certification: {url}"
                    )

            # 4. Date consistency
            if issue and expiry:
                self._validate_dates(issue, expiry, f"{prefix}.dates", errors)

        return errors

    def _validate_dates(
        self,
        start: str,
        end: str,
        key: str,
        errors: dict[str, list[str]],
    ) -> None:
        """Helper to validate issue and expiration date consistency."""
        year_re = re.compile(r"\b(19\d{2}|2\d{3})\b")
        start_years = year_re.findall(start)
        end_years = year_re.findall(end)

        if start_years and end_years:
            start_yr = int(start_years[0])
            end_yr = int(end_years[0])
            if start_yr > end_yr:
                errors.setdefault(key, []).append(
                    f"Issue year ({start_yr}) cannot be "
                    f"after expiration year ({end_yr})"
                )
