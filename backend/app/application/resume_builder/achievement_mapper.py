"""Mapper for extracting and parsing achievements from the CIR."""

import re
from typing import Any

from app.domain.entities.canonical_intermediate_representation import (
    CanonicalIntermediateRepresentation,
)
from app.domain.entities.section_type import SectionType


class AchievementMapper:
    """Mapper class that parses section content into structured achievement records."""

    YEAR_PATTERN = re.compile(r"\b(19\d{2}|2\d{3})\b")

    def map_cir_to_achievement_records(
        self,
        cir: CanonicalIntermediateRepresentation,
    ) -> list[dict[str, Any]]:
        """Find and parse all achievements inside the CIR.

        Args:
            cir: The source Canonical Intermediate Representation.

        Returns:
            A list of dictionary objects representing mapped raw achievement records.
        """
        records: list[dict[str, Any]] = []

        ach_sections = [
            sec for sec in cir.sections if sec.section_type == SectionType.ACHIEVEMENTS
        ]
        if not ach_sections:
            return records

        for sec in ach_sections:
            lines = [line.strip() for line in sec.content.split("\n") if line.strip()]
            for line in lines:
                parsed = self._parse_achievement_line(line)
                if parsed:
                    records.append(parsed)

        return records

    def _parse_achievement_line(self, line: str) -> dict[str, Any] | None:
        """Heuristically parse a single line representing an achievement."""
        # Strip leading numbers followed by dot/space, and bullets
        clean_line = re.sub(r"^[•\-\*\d\s\.]+\s*", "", line).strip()
        if not clean_line:
            return None

        # Extract dates
        date = None
        years = self.YEAR_PATTERN.findall(clean_line)
        if years:
            date = years[0]
            # Strip years from the name to avoid putting them in title/desc
            for y in years:
                clean_line = re.sub(rf"\b{y}\b", "", clean_line).strip("() ")

        title = clean_line
        description = ""

        # Split by separator to get title and description
        parts = []
        if " - " in clean_line:
            parts = [p.strip() for p in clean_line.split(" - ") if p.strip()]
        elif " | " in clean_line:
            parts = [p.strip() for p in clean_line.split(" | ") if p.strip()]
        elif " : " in clean_line:
            parts = [p.strip() for p in clean_line.split(" : ") if p.strip()]
        elif "," in clean_line:
            parts = [p.strip() for p in clean_line.split(",", 1) if p.strip()]

        if len(parts) >= 2:
            title = parts[0]
            description = parts[1]
        else:
            title = clean_line
            description = clean_line

        # Final sanitization
        title = " ".join(title.strip(" \t\n\r,;:|–-").split())
        description = " ".join(description.strip(" \t\n\r,;:|–-").split())

        return {
            "title": title,
            "description": description if description else None,
            "date": date,
        }
