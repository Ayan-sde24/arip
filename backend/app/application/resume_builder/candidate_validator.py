"""Validator for checking Candidate fields and constraints."""

import re
from typing import Any


class CandidateValidationError(Exception):
    """Exception raised when candidate validation fails."""

    pass


class CandidateValidator:
    """Validator for verifying Candidate fields and constraints."""

    # Simple email pattern
    EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    # Simple phone pattern: digits, spaces, hyphens, parenthesis, optional +
    PHONE_REGEX = re.compile(r"^\+?[\d\s\-()]{7,20}$")
    # URL pattern starting with http://, https://, or www.
    URL_REGEX = re.compile(r"^(https?://)?(www\.)?[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")

    def validate(self, data: dict[str, Any]) -> dict[str, list[str]]:
        """Validate candidate dictionary fields and return map of errors.

        Args:
            data: Raw mapped candidate fields dictionary.

        Returns:
            A dictionary mapping field names to lists of error messages.
        """
        errors: dict[str, list[str]] = {}

        # 1. Name Validation
        name = data.get("name")
        if not name:
            errors.setdefault("name", []).append("Name is required")
        elif len(name.strip()) < 2:
            errors.setdefault("name", []).append(
                "Name must be at least 2 characters long"
            )

        # 2. Email Validation
        email = data.get("email")
        if not email:
            errors.setdefault("email", []).append("Email is required")
        else:
            email_str = str(email).strip()
            # Check for multiple/duplicate emails
            parts = email_str.split()
            if len(parts) > 1:
                if len(set(parts)) != len(parts):
                    errors.setdefault("email", []).append(
                        "Duplicate email addresses detected"
                    )
                else:
                    errors.setdefault("email", []).append(
                        "Multiple distinct emails detected"
                    )

            # Validate each email part format
            for part in parts:
                if not self.EMAIL_REGEX.match(part):
                    errors.setdefault("email", []).append(
                        f"Invalid email format: {part}"
                    )

        # 3. Phone Validation
        phone = data.get("phone")
        if not phone:
            errors.setdefault("phone", []).append("Phone is required")
        else:
            phone_str = str(phone).strip()
            if not self.PHONE_REGEX.match(phone_str):
                errors.setdefault("phone", []).append("Invalid phone format")

        # 4. URL fields validation (LinkedIn, GitHub, Portfolio)
        for url_field in ("linkedin", "github", "portfolio"):
            val = data.get(url_field)
            if val:
                val_str = str(val).strip()
                if not self.URL_REGEX.match(val_str):
                    errors.setdefault(url_field, []).append(
                        f"Invalid URL format for {url_field}"
                    )

        return errors
