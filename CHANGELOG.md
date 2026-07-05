# Changelog

## 0.3.0 - Universal Document Domain Model

- Established the core Domain Layer for the platform (`backend/app/domain/entities`).
- Implemented immutable `Document` and `Candidate` domain entities using Python standard library `dataclasses`.
- Implemented `DocumentStatus` and `DocumentType` enums using `StrEnum`.
- Implemented `Resume` business entity composed of `Document`, `Candidate`, and structured sub-collections (`Education`, `Experience`, `Project`, `Certification`, `Achievement`).
- Implemented `JobDescription` business entity composed of `Document`, requirements, responsibilities, and preferred skills.
- Implemented `AnalysisContext` to act as the standard communication payload shared across all AI agents.
- Implemented `AgentResult`, `Evidence`, and `Recommendation` entities to support multi-agent orchestrations and explainable decision support.
- Added comprehensive unit tests for all domain entities, validation states, and immutability guarantees.

## 0.2.0 - Document Storage Foundation

- Added reusable document storage module with provider interface.
- Added filesystem storage provider for local uploads.
- Added validation for file size, extension, MIME type, hidden extensions, executable extensions, and empty files.
- Added UUID-based stored filenames and SHA-256 checksum generation.
- Added `/api/v1/upload/resume` endpoint returning standardized upload responses.
- Added unit tests for valid uploads, invalid inputs, checksum generation, UUID filenames, and duplicate uploads.
- Updated configuration and documentation for upload validation settings.
