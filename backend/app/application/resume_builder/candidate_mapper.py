"""Mapper for extracting and normalizing candidate information from the CIR."""

import re
from typing import Any

from app.domain.entities.canonical_intermediate_representation import (
    CanonicalIntermediateRepresentation,
)
from app.domain.entities.section_type import SectionType


class CandidateMapper:
    """Mapper class that extracts candidate contact details from the CIR."""

    EMAIL_PATTERN = re.compile(r"[\w\.-]+@[\w\.-]+\.\w+")
    # Matches typical formats: +1 (555) 019-2834, 555.019.2834, +44 20 7946 0929
    PHONE_PATTERN = re.compile(
        r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{4}"
    )

    def map_cir_to_candidate_data(
        self,
        cir: CanonicalIntermediateRepresentation,
    ) -> dict[str, Any]:
        """Scan CIR sections and document content to extract candidate properties.

        Args:
            cir: The source Canonical Intermediate Representation.

        Returns:
            A dict containing raw extracted candidate properties.
        """
        # Find contact sections
        contact_blocks = []
        for sec in cir.sections:
            if sec.section_type == SectionType.CONTACT:
                contact_blocks.extend(sec.content.split("\n"))

        # Fallback to top raw document text blocks if no contact section is present
        if not contact_blocks:
            for page in cir.document_content.pages:
                for block in page.text_blocks[:5]:
                    contact_blocks.append(block.text)

        # Join contact blocks into lines
        lines = [line.strip() for line in contact_blocks if line.strip()]
        full_text = "\n".join(lines)

        # 1. Extract Email
        emails = self.EMAIL_PATTERN.findall(full_text)
        email = " ".join(emails) if emails else ""

        # 2. Extract Phone
        phones = self.PHONE_PATTERN.findall(full_text)
        phone = phones[0].strip() if phones else ""

        # 3. Extract URLs
        linkedin = ""
        github = ""
        portfolio = ""

        # Find all words that look like links
        words = full_text.split()
        for word in words:
            word_clean = word.strip("(),;<>\"'")
            if "linkedin.com" in word_clean.lower():
                linkedin = word_clean
            elif "github.com" in word_clean.lower():
                github = word_clean
            elif (
                word_clean.lower().startswith(("http://", "https://", "www."))
                and "linkedin.com" not in word_clean.lower()
                and "github.com" not in word_clean.lower()
            ):
                portfolio = word_clean

        # 4. Extract Location
        location = ""
        # Check lines for city, state pattern (e.g. Dallas, TX or San Francisco, CA)
        city_state_pattern = re.compile(r"^[A-Za-z\s\.\'-]+,\s*[A-Z]{2}(?:\s+\d{5})?$")
        city_country_pattern = re.compile(r"^[A-Za-z\s\.\'-]+,\s*[A-Za-z\s\.\'-]+$")
        for line in lines:
            if city_state_pattern.match(line):
                location = line
                break
        if not location:
            # Fallback to line with comma that isn't name, email, URL or phone
            for line in lines:
                if (
                    "," in line
                    and not self.EMAIL_PATTERN.search(line)
                    and not any(
                        k in line.lower() for k in ("http", "www", "github", "linkedin")
                    )
                ):
                    if city_country_pattern.match(line) and len(line) < 40:
                        location = line
                        break

        # 5. Extract Name
        name = ""
        for line in lines:
            # Exclude lines that contain email, phone digits, or links
            if (
                not self.EMAIL_PATTERN.search(line)
                and not self.PHONE_PATTERN.search(line)
                and not any(
                    k in line.lower() for k in ("http", "www", "github", "linkedin")
                )
                and len(line.split()) <= 4
                and any(c.isalpha() for c in line)
            ):
                # Clean up any potential metadata like '(alice@example.com)' or similar
                clean_name = re.sub(r"\(.*?\)", "", line).strip()
                if clean_name:
                    name = self.normalize_string(clean_name)
                    break

        return {
            "name": name,
            "email": email,
            "phone": phone,
            "linkedin": linkedin if linkedin else None,
            "github": github if github else None,
            "portfolio": portfolio if portfolio else None,
            "location": location if location else None,
        }

    def normalize_string(self, text: str) -> str:
        """Remove duplicate whitespaces and strip string."""
        if not text:
            return ""
        return " ".join(text.split())
