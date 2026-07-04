"""Custom exceptions raised by the document storage module."""


class StorageError(Exception):
    """Base exception for storage module failures."""


class StorageValidationError(StorageError):
    """Raised when an uploaded document fails validation."""


class UnsupportedFileTypeError(StorageValidationError):
    """Raised when a file extension is not supported."""


class FileTooLargeError(StorageValidationError):
    """Raised when a file exceeds the configured maximum size."""


class InvalidMimeTypeError(StorageValidationError):
    """Raised when a file MIME type is not allowed."""


class EmptyFileError(StorageValidationError):
    """Raised when an uploaded file has no content."""


class HiddenExtensionError(StorageValidationError):
    """Raised when a filename contains a hidden or double extension."""


class StorageProviderError(StorageError):
    """Raised when the configured storage provider fails."""
