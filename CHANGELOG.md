# Changelog

## 0.2.0 - Document Storage Foundation

- Added reusable document storage module with provider interface.
- Added filesystem storage provider for local uploads.
- Added validation for file size, extension, MIME type, hidden extensions, executable extensions, and empty files.
- Added UUID-based stored filenames and SHA-256 checksum generation.
- Added `/api/v1/upload/resume` endpoint returning standardized upload responses.
- Added unit tests for valid uploads, invalid inputs, checksum generation, UUID filenames, and duplicate uploads.
- Updated configuration and documentation for upload validation settings.
