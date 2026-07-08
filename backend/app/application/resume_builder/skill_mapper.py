"""Mapper for extracting and parsing skills from the CIR."""

import re
from typing import Any

from app.domain.entities.canonical_intermediate_representation import (
    CanonicalIntermediateRepresentation,
)
from app.domain.entities.section_type import SectionType


class SkillMapper:
    """Mapper class that parses section content into structured skill records."""

    def map_cir_to_skill_records(
        self,
        cir: CanonicalIntermediateRepresentation,
    ) -> list[dict[str, Any]]:
        """Find and parse all skills inside the CIR.

        Args:
            cir: The source Canonical Intermediate Representation.

        Returns:
            A list of dictionary objects representing mapped raw skill records.
        """
        records: list[dict[str, Any]] = []

        skill_sections = [
            sec for sec in cir.sections if sec.section_type == SectionType.SKILLS
        ]
        if not skill_sections:
            return records

        for sec in skill_sections:
            lines = [line.strip() for line in sec.content.split("\n") if line.strip()]
            for line in lines:
                category = None
                skills_part = line

                # Check for category header, e.g. "Languages: Python, Go"
                category_match = re.match(r"^([^:(]+):\s*(.*)$", line)
                if category_match:
                    category = category_match.group(1).strip()
                    skills_part = category_match.group(2).strip()

                # Split by comma or semicolon
                parts = re.split(r"[,;]", skills_part)
                for part in parts:
                    part_clean = part.strip(" \t\n\r.*•-")
                    if not part_clean:
                        continue

                    name = part_clean
                    proficiency = None

                    # Check for parenthesized proficiency, e.g. "Python (Advanced)"
                    prof_match = re.match(r"^(.*?)\s*\(([^)]+)\)$", part_clean)
                    if prof_match:
                        name = prof_match.group(1).strip()
                        proficiency = prof_match.group(2).strip()

                    name_norm = " ".join(name.split())
                    if not name_norm:
                        continue

                    records.append(
                        {
                            "name": name_norm,
                            "category": category if category else None,
                            "proficiency": proficiency if proficiency else None,
                        }
                    )

        return records
