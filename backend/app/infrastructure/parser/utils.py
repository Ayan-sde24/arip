"""Shared utility functions for the document intelligence pipeline."""

import re
import unicodedata

from app.infrastructure.parser.models import DocumentStatistics

# Regex compiled once at module load for efficiency
_CONTROL_CHAR_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
_MULTI_WHITESPACE_RE = re.compile(r"[^\S\n]+")
_MULTI_NEWLINE_RE = re.compile(r"\n{3,}")


def clean_text(raw: str) -> str:
    """Normalize whitespace and strip control characters from raw document text.

    Applies the following transformations in order:
    1. Unicode NFC normalization.
    2. Strip C0/C1 control characters (except \\n and \\t).
    3. Collapse multiple spaces/tabs on a single line to one space.
    4. Collapse 3+ consecutive newlines to 2 newlines.
    5. Strip leading/trailing whitespace.

    Args:
        raw: The raw text string to clean.

    Returns:
        A cleaned, normalized text string.
    """
    text = unicodedata.normalize("NFC", raw)
    text = _CONTROL_CHAR_RE.sub("", text)
    text = _MULTI_WHITESPACE_RE.sub(" ", text)
    text = _MULTI_NEWLINE_RE.sub("\n\n", text)
    return text.strip()


def compute_statistics(
    raw_text: str,
    page_count: int,
) -> DocumentStatistics:
    """Compute quantitative metrics from document text.

    Args:
        raw_text: The full raw document text (all pages concatenated).
        page_count: Number of pages in the document.

    Returns:
        A :class:`DocumentStatistics` instance with computed metrics.
    """
    words = raw_text.split()
    word_count = len(words)
    char_count = len(raw_text)
    avg_words = word_count / page_count if page_count > 0 else 0.0
    return DocumentStatistics(
        page_count=page_count,
        word_count=word_count,
        char_count=char_count,
        avg_words_per_page=round(avg_words, 2),
    )


def detect_language(text: str) -> str:  # noqa: ARG001
    """Return the detected language code for the given text.

    This is a placeholder for future language detection integration
    (e.g. ``langdetect`` or ``lingua``). Until wired in, returns
    ``"unknown"`` for all inputs.

    Args:
        text: Text content to analyse.

    Returns:
        A BCP-47 language code string, or ``"unknown"``.
    """
    return "unknown"
