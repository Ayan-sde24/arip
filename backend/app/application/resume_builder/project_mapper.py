"""Mapper for extracting and parsing projects from the CIR."""

import re
from typing import Any

from app.domain.entities.canonical_intermediate_representation import (
    CanonicalIntermediateRepresentation,
)
from app.domain.entities.section_type import SectionType


class ProjectMapper:
    """Mapper class that parses section content into structured project records."""

    URL_PATTERN = re.compile(
        r"https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\b[-a-zA-Z0-9@:%_\+.~#?&//=]*"
    )

    def map_cir_to_project_records(
        self,
        cir: CanonicalIntermediateRepresentation,
    ) -> list[dict[str, Any]]:
        """Find and parse all project records inside the CIR.

        Args:
            cir: The source Canonical Intermediate Representation.

        Returns:
            A list of dictionary objects representing mapped raw project records.
        """
        records: list[dict[str, Any]] = []

        proj_sections = [
            sec for sec in cir.sections if sec.section_type == SectionType.PROJECTS
        ]
        if not proj_sections:
            return records

        for sec in proj_sections:
            # Split by double newline or blank lines
            blocks = [b.strip() for b in sec.content.split("\n\n") if b.strip()]
            # Fallback to single newlines if only single newlines
            # are present and they start with bullets
            if len(blocks) == 1:
                lines = [
                    line.strip() for line in sec.content.split("\n") if line.strip()
                ]
                if all(
                    line.startswith(("-", "*", "•", "1.", "2.")) for line in lines[1:]
                ):
                    # Every bullet line could be a separate project
                    blocks = lines

            for block in blocks:
                lines = [line.strip() for line in block.split("\n") if line.strip()]
                if not lines:
                    continue
                parsed = self._parse_project_lines(lines)
                records.append(parsed)

        return records

    def _parse_project_lines(self, lines: list[str]) -> dict[str, Any]:
        """Heuristically extract project details from lines."""
        title_line = lines[0]
        url = ""
        skills: list[str] = []
        desc_lines: list[str] = []

        # Extract URL from title line if present in parentheses
        url_match = self.URL_PATTERN.search(title_line)
        if url_match:
            url = url_match.group(0)
            # Remove URL and parentheses from title
            clean_title = re.sub(
                r"\s*\(?\s*" + re.escape(url) + r"\s*\)?", "", title_line
            ).strip()
            title = clean_title.strip(":- ")
        else:
            title = title_line.strip(":-*• ")

        for line in lines[1:]:
            # Check for URL if not already found
            if not url:
                line_url_match = self.URL_PATTERN.search(line)
                if line_url_match:
                    url = line_url_match.group(0)
                    continue

            # Check for skills/technologies
            lower_line = line.lower()
            if any(
                k in lower_line
                for k in ("skills:", "technologies:", "tech stack:", "built with:")
            ):
                if ":" in line:
                    tech_part = line.split(":", 1)[1]
                    skills.extend(
                        [s.strip() for s in tech_part.split(",") if s.strip()]
                    )
                else:
                    tech_part = re.sub(
                        r"^(?:skills|technologies|tech stack|built with)\s+",
                        "",
                        line,
                        flags=re.IGNORECASE,
                    )
                    skills.extend(
                        [s.strip() for s in tech_part.split(",") if s.strip()]
                    )
                continue

            desc_lines.append(line)

        description = " ".join(desc_lines) if desc_lines else ""

        return {
            "title": title,
            "description": description if description else None,
            "url": url if url else None,
            "skills": skills,
        }
