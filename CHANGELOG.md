# Changelog

## 0.7.0 - Section Boundary Detection Engine

- Implemented `SectionBoundary` model holding segment coordinates (start/end page/block indices, heading reference, confidence, evidence, and metadata).
- Implemented `BoundaryRule` base class and concrete boundary scoring rules (`NextHeadingBoundaryRule`, `EndOfDocumentBoundaryRule`, `PageBreakBoundaryRule`, `EmptyLineBoundaryRule`).
- Implemented `BoundaryDetector` service grouping heading candidates and resolving start/end offsets sequentially across the document pages.
- Added unit tests for single section documents, multi-section boundaries, repeated headings, trailing sections, page break alignments, and documents without headings.

## 0.6.0 - Heading Detection Engine


- Implemented `HeadingCandidate` model representing heading blocks found in documents.
- Implemented `HeadingRule` base class and concrete scoring rule engines (`LengthRule`, `CapitalizationRule`, `WhitespaceRule`, `KeywordRule`, `PositionRule`).
- Implemented `HeadingDetector` service mapping over document pages to evaluate, combine, and score block heuristics to return identified heading candidates.
- Added unit tests for standard keyword headings, unknown headings (heuristic-based), lowercase headings, repeated headings, empty document handling, and filtering false positives.

## 0.5.0 - Section Type Domain Model


- Implemented `SectionType` StrEnum defining categories of document sections (`SUMMARY`, `PROFILE`, `OBJECTIVE`, `EDUCATION`, `EXPERIENCE`, `PROJECTS`, `SKILLS`, `CERTIFICATIONS`, `ACHIEVEMENTS`, `PUBLICATIONS`, `LANGUAGES`, `CONTACT`, `INTERESTS`, `VOLUNTEER`, `AWARDS`, `OTHER`, `UNKNOWN`).
- Implemented immutable `DocumentSection` domain entity wrapping section data (id, type, title, content, page/block ranges, confidence, and metadata).
- Implemented immutable `StructuredDocument` domain entity containing the source document and list of sections, including section lookup methods (`get_section`, `find_sections`, `has_section`).
- Integrated and exported the new domain models in the domain layer.
- Added unit tests covering the section domain models and lookup methods.

## 0.4.0 - Document Intelligence Pipeline


- Implemented three-stage `DocumentIntelligencePipeline` in `backend/app/infrastructure/parser/`.
- **Stage 1 — Read**: `PdfReader` (PyMuPDF) extracts pages, text blocks, and bounding boxes. `DocxReader` (python-docx) extracts paragraphs with page-break-aware splitting.
- **Stage 2 — Layout Analysis**: `LayoutAnalyzer` converts raw reader output into immutable `Page` and `TextBlock` domain objects with globally monotonic `reading_order` indices.
- **Stage 3 — Build**: `DocumentContentBuilder` assembles the final `DocumentContent` domain object with raw text, cleaned text, metadata, language placeholder, and computed statistics.
- Added three new domain entities: `DocumentContent`, `Page`, `TextBlock`.
- Added custom exception hierarchy: `ParserError`, `UnreadablePDFError`, `CorruptedDocxError`, `EmptyDocumentError`, `UnsupportedEncodingError`, `ReaderFailureError`.
- Added `DocumentReader` Protocol interface for future extensibility (OCR, HTML, Markdown, LinkedIn export).
- Added shared utilities: `clean_text()`, `compute_statistics()`, `detect_language()` (placeholder).
- Added 32 unit tests covering domain entities, readers, layout analysis, and end-to-end pipeline runs.
- Pipeline has no AI, NLP, or embedding dependencies.

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
