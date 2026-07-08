"""Mapper for extracting and parsing work experience records from the CIR."""

import re
from typing import Any

from app.domain.entities.canonical_intermediate_representation import (
    CanonicalIntermediateRepresentation,
)
from app.domain.entities.section_type import SectionType


class ExperienceMapper:
    """Mapper class that parses section content into experience records."""

    ROLE_KEYWORDS = [
        "engineer",
        "developer",
        "manager",
        "analyst",
        "lead",
        "director",
        "architect",
        "intern",
        "specialist",
        "consultant",
        "designer",
        "coordinator",
        "administrator",
    ]

    YEAR_PATTERN = re.compile(r"\b(19\d{2}|2\d{3})\b")

    def map_cir_to_experience_records(
        self,
        cir: CanonicalIntermediateRepresentation,
    ) -> list[dict[str, Any]]:
        """Find and parse all experience records inside the CIR.

        Args:
            cir: The source Canonical Intermediate Representation.

        Returns:
            A list of dictionary objects representing mapped raw experience records.
        """
        records: list[dict[str, Any]] = []

        exp_sections = [
            sec for sec in cir.sections if sec.section_type == SectionType.EXPERIENCE
        ]
        if not exp_sections:
            return records

        for sec in exp_sections:
            lines = [line.strip() for line in sec.content.split("\n") if line.strip()]
            if not lines:
                continue

            grouped_records: list[list[str]] = []
            current_rec: list[str] = []

            # Split when encountering a line starting a new experience
            for line in lines:
                is_new = False
                if not line.startswith(("-", "*", "•", "1.", "2.")):
                    # Match only full words to avoid false positive matches
                    words = set(re.findall(r"\b\w+\b", line.lower()))
                    has_role = (
                        any(kw in words for kw in self.ROLE_KEYWORDS) and len(line) < 60
                    )
                    has_company_suffix = any(
                        re.search(rf"\b{s}\b", line, re.IGNORECASE)
                        for s in ["Inc", "Corp", "Ltd", "LLC", "Co"]
                    )

                    if has_role or has_company_suffix:
                        is_new = True

                if is_new and current_rec:
                    grouped_records.append(current_rec)
                    current_rec = [line]
                else:
                    if current_rec:
                        current_rec.append(line)
                    else:
                        current_rec = [line]
            if current_rec:
                grouped_records.append(current_rec)

            for record_lines in grouped_records:
                parsed = self._parse_record_lines(record_lines)
                records.append(parsed)

        return records

    def _parse_record_lines(self, lines: list[str]) -> dict[str, Any]:
        """Heuristically extract work experience details from text lines."""
        company = ""
        role = ""
        location = ""
        start_date = ""
        end_date = ""
        current_position = False
        description: list[str] = []
        skills: list[str] = []

        first_line = lines[0]
        # Check first line for dates
        years_first = self.YEAR_PATTERN.findall(first_line)
        if years_first:
            if len(years_first) >= 2:
                start_date = years_first[0]
                end_date = years_first[1]
            elif len(years_first) == 1:
                start_date = years_first[0]
                if any(p in first_line.lower() for p in ("present", "current", "now")):
                    end_date = "Present"
                    current_position = True
                else:
                    end_date = years_first[0]

        if " | " in first_line:
            parts = first_line.split(" | ")
            if len(parts) >= 2:
                company = parts[0].strip()
                role = parts[1].strip()
                if len(parts) >= 3:
                    if not self.YEAR_PATTERN.search(parts[2]):
                        location = parts[2].strip()
        elif " - " in first_line or " – " in first_line:
            sep = " - " if " - " in first_line else " – "
            parts = first_line.split(sep, 1)
            p0_has_role = any(kw in parts[0].lower() for kw in self.ROLE_KEYWORDS)
            if p0_has_role:
                role = parts[0].strip()
                company = parts[1].strip()
            else:
                company = parts[0].strip()
                role = parts[1].strip()

        for line in lines[1:]:
            years = self.YEAR_PATTERN.findall(line)
            if years and not start_date:
                if len(years) >= 2:
                    start_date = years[0]
                    end_date = years[1]
                elif len(years) == 1:
                    start_date = years[0]
                    if any(p in line.lower() for p in ("present", "current", "now")):
                        end_date = "Present"
                        current_position = True
                    else:
                        end_date = years[0]

                date_line_lower = line.lower()
                for month in (
                    "jan",
                    "feb",
                    "mar",
                    "apr",
                    "may",
                    "jun",
                    "jul",
                    "aug",
                    "sep",
                    "oct",
                    "nov",
                    "dec",
                ):
                    if month in date_line_lower:
                        parts = line.split("-")
                        if len(parts) == 2:
                            start_date = parts[0].strip()
                            end_date = parts[1].strip()
                            if any(
                                p in parts[1].lower()
                                for p in ("present", "current", "now")
                            ):
                                current_position = True
                        break
                continue

            city_state_pattern = re.compile(
                r"^[A-Za-z\s\.\'-]+,\s*[A-Z]{2}(?:\s+\d{5})?$"
            )
            if city_state_pattern.match(line) and not location:
                location = line
                continue

            has_role_kw = any(kw in line.lower() for kw in self.ROLE_KEYWORDS)
            if has_role_kw and not role and len(line) < 50:
                role = line
                continue

            if (
                "technologies" in line.lower()
                or "skills:" in line.lower()
                or "tech stack" in line.lower()
            ):
                if ":" in line:
                    tech_part = line.split(":", 1)[1]
                    skills.extend(
                        [s.strip() for s in tech_part.split(",") if s.strip()]
                    )
                continue

            description.append(line)

        if not company:
            company = first_line
        if not role:
            if len(lines) > 1 and len(lines[1]) < 50:
                role = lines[1]
            else:
                role = "Software Engineer"

        if end_date.lower() in ("present", "current", "now"):
            current_position = True

        return {
            "company": company,
            "role": role,
            "location": location if location else None,
            "start_date": start_date if start_date else None,
            "end_date": end_date if end_date else None,
            "current_position": current_position,
            "description": description,
            "skills": skills,
        }
