"""Mapper for extracting and parsing educational records from the CIR."""

import re
from typing import Any

from app.domain.entities.canonical_intermediate_representation import (
    CanonicalIntermediateRepresentation,
)
from app.domain.entities.section_type import SectionType


class EducationMapper:
    """Mapper class that parses section content into structured educational records."""

    INSTITUTION_KEYWORDS = [
        "university",
        "college",
        "institute",
        "school",
        "academy",
        "polytechnic",
        "mit",
        "caltech",
        "iit",
        "stanford",
        "harvard",
        "yale",
        "princeton",
    ]

    DEGREE_KEYWORDS = [
        "bachelor",
        "master",
        "doctor",
        "phd",
        "bs",
        "ms",
        "ba",
        "ma",
        "btech",
        "mtech",
        "mba",
        "diploma",
        "degree",
        "associate",
    ]

    YEAR_PATTERN = re.compile(r"\b(19\d{2}|2\d{3})\b")
    GPA_PATTERN = re.compile(r"(?:gpa|cgpa)[:\s]*([0-9.]+)(?:/[0-9.]+)?", re.IGNORECASE)

    def map_cir_to_education_records(
        self,
        cir: CanonicalIntermediateRepresentation,
    ) -> list[dict[str, Any]]:
        """Find and parse all education records inside the CIR.

        Args:
            cir: The source Canonical Intermediate Representation.

        Returns:
            A list of dictionary objects representing mapped raw educational records.
        """
        records: list[dict[str, Any]] = []

        edu_sections = [
            sec for sec in cir.sections if sec.section_type == SectionType.EDUCATION
        ]
        if not edu_sections:
            return records

        for sec in edu_sections:
            lines = [line.strip() for line in sec.content.split("\n") if line.strip()]
            if not lines:
                continue

            grouped_records: list[list[str]] = []
            current_rec: list[str] = []

            for line in lines:
                is_inst = any(kw in line.lower() for kw in self.INSTITUTION_KEYWORDS)
                if is_inst:
                    if current_rec:
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
        """Heuristically extract educational details from grouped text lines."""
        institution = lines[0]
        degree = ""
        major = ""
        start_date = ""
        end_date = ""
        gpa = None
        details: list[str] = []

        for line in lines[1:]:
            gpa_match = self.GPA_PATTERN.search(line)
            if gpa_match:
                try:
                    gpa = float(gpa_match.group(1))
                except ValueError:
                    pass
                if len(line) < 15:
                    continue

            years = self.YEAR_PATTERN.findall(line)
            if years:
                if len(years) >= 2:
                    start_date = years[0]
                    end_date = years[1]
                elif len(years) == 1:
                    start_date = years[0]
                    if any(p in line.lower() for p in ("present", "current", "now")):
                        end_date = "Present"
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
                        break
                continue

            has_deg_kw = any(kw in line.lower() for kw in self.DEGREE_KEYWORDS)
            if has_deg_kw and not degree:
                if " in " in line:
                    parts = line.split(" in ", 1)
                    degree = parts[0].strip()
                    major = parts[1].strip()
                elif " major " in line.lower():
                    parts = re.split(r"\s+major\s+", line, flags=re.IGNORECASE)
                    degree = parts[0].strip()
                    major = parts[1].strip()
                else:
                    degree = line
                continue

            details.append(line)

        if not degree and len(lines) > 1:
            second_line = lines[1]
            if not start_date and not gpa:
                degree = second_line

        return {
            "institution": institution,
            "degree": degree if degree else None,
            "major": major if major else None,
            "start_date": start_date if start_date else None,
            "end_date": end_date if end_date else None,
            "gpa": gpa,
            "details": details,
        }
