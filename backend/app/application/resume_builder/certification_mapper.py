"""Mapper for extracting and parsing certifications from the CIR."""

import re
from typing import Any

from app.domain.entities.canonical_intermediate_representation import (
    CanonicalIntermediateRepresentation,
)
from app.domain.entities.section_type import SectionType


class CertificationMapper:
    """Mapper class that parses section content into certification records."""

    YEAR_PATTERN = re.compile(r"\b(19\d{2}|2\d{3})\b")
    URL_PATTERN = re.compile(
        r"https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\b[-a-zA-Z0-9@:%_\+.~#?&//=]*"
    )

    def map_cir_to_certification_records(
        self,
        cir: CanonicalIntermediateRepresentation,
    ) -> list[dict[str, Any]]:
        """Find and parse all certification records inside the CIR.

        Args:
            cir: The source Canonical Intermediate Representation.

        Returns:
            A list of dictionary objects representing mapped raw certification records.
        """
        records: list[dict[str, Any]] = []

        cert_sections = [
            sec
            for sec in cir.sections
            if sec.section_type == SectionType.CERTIFICATIONS
        ]
        if not cert_sections:
            return records

        for sec in cert_sections:
            lines = [line.strip() for line in sec.content.split("\n") if line.strip()]
            for line in lines:
                parsed = self._parse_certification_line(line)
                if parsed:
                    records.append(parsed)

        return records

    def _parse_certification_line(self, line: str) -> dict[str, Any] | None:
        """Heuristically parse a single line representing a certification."""
        # Strip leading numbers followed by dot/space, and bullets
        clean_line = re.sub(r"^[•\-\*\d\s\.]+\s*", "", line).strip()
        if not clean_line:
            return None

        url = None
        # Extract URL
        url_match = self.URL_PATTERN.search(clean_line)
        if url_match:
            url = url_match.group(0)
            clean_line = clean_line.replace(url, "").strip("()[] ")

        issue_date = None
        expiration_date = None

        # Extract dates
        years = self.YEAR_PATTERN.findall(clean_line)
        if years:
            if len(years) >= 2:
                issue_date = years[0]
                expiration_date = years[1]
            elif len(years) == 1:
                issue_date = years[0]
                if any(
                    k in clean_line.lower()
                    for k in ("expiry", "expires", "valid until")
                ):
                    expiration_date = years[0]
                    issue_date = None

        # Split by separator to get name and issuer
        parts = re.split(r"\s*(?:\||-|–)\s*", clean_line)
        parts = [p.strip() for p in parts if p.strip()]

        # Filter out years or date parts
        non_date_parts = []
        for p in parts:
            if self.YEAR_PATTERN.search(p) or not p:
                continue
            non_date_parts.append(p)

        name = ""
        issuer = None

        if len(non_date_parts) >= 2:
            name = non_date_parts[0]
            issuer = non_date_parts[1]
        elif non_date_parts:
            name = non_date_parts[0]

        # Final sanitization
        name = " ".join(name.strip(" \t\n\r,;:|–-").split())
        if issuer:
            issuer = " ".join(issuer.strip(" \t\n\r,;:|–-").split())

        return {
            "name": name,
            "issuer": issuer if issuer else None,
            "issue_date": issue_date,
            "expiration_date": expiration_date,
            "url": url,
        }
