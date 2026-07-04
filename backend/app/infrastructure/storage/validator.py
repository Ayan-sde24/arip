"""Validation rules for uploaded documents."""

from pathlib import PurePath

from app.core.logger import get_logger
from app.infrastructure.storage.exceptions import (
    EmptyFileError,
    FileTooLargeError,
    HiddenExtensionError,
    InvalidMimeTypeError,
    UnsupportedFileTypeError,
)

logger = get_logger(__name__)

EXECUTABLE_EXTENSIONS = {
    "bat",
    "cmd",
    "com",
    "dll",
    "exe",
    "js",
    "msi",
    "ps1",
    "scr",
    "sh",
    "vbs",
}


class FileValidator:
    """Validate uploaded file metadata before persistence."""

    def __init__(
        self,
        *,
        allowed_extensions: tuple[str, ...],
        allowed_mime_types: tuple[str, ...],
        max_size_bytes: int,
    ) -> None:
        """Initialize validation constraints."""
        self._allowed_extensions = {
            extension.lower().lstrip(".") for extension in allowed_extensions
        }
        self._allowed_mime_types = set(allowed_mime_types)
        self._max_size_bytes = max_size_bytes

    def validate(self, *, filename: str, mime_type: str, size: int) -> str:
        """Validate file attributes and return the normalized extension."""
        suffixes = [
            suffix.lower().lstrip(".") for suffix in PurePath(filename).suffixes
        ]
        extension = suffixes[-1] if suffixes else ""

        if size == 0:
            logger.warning(
                "Validation failure: empty file {filename}",
                filename=filename,
            )
            raise EmptyFileError("Empty file")

        if size > self._max_size_bytes:
            logger.warning(
                "Validation failure: file too large {filename}",
                filename=filename,
            )
            raise FileTooLargeError("File too large")

        if not extension or extension not in self._allowed_extensions:
            logger.warning(
                "Validation failure: unsupported file type {filename}",
                filename=filename,
            )
            raise UnsupportedFileTypeError("Unsupported file type")

        if len(suffixes) > 1:
            logger.warning(
                "Validation failure: hidden extension {filename}",
                filename=filename,
            )
            raise HiddenExtensionError("Unsupported file type")

        if any(suffix in EXECUTABLE_EXTENSIONS for suffix in suffixes):
            logger.warning(
                "Validation failure: executable extension {filename}",
                filename=filename,
            )
            raise UnsupportedFileTypeError("Unsupported file type")

        if mime_type not in self._allowed_mime_types:
            logger.warning(
                "Validation failure: invalid MIME {mime_type}",
                mime_type=mime_type,
            )
            raise InvalidMimeTypeError("Invalid MIME")

        logger.info("Validation success for {filename}", filename=filename)
        return extension
