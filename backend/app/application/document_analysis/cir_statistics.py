"""Model representing statistics for the Canonical Intermediate Representation."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CIRStatistics:
    """Statistics calculated during CIR assembly.

    Attributes:
        total_pages: Total number of pages in the document.
        total_sections: Total number of detected sections.
        total_text_blocks: Total number of text blocks across pages.
        total_characters: Total characters count across text blocks.
        total_words: Total words count across text blocks.
        detected_languages: List of detected languages.
        average_section_length: Average character length of sections.
    """

    total_pages: int
    total_sections: int
    total_text_blocks: int
    total_characters: int
    total_words: int
    detected_languages: list[str]
    average_section_length: float
