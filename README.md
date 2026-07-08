# ARIP Backend

ARIP is an enterprise AI Resume Intelligence Platform. This repository contains the backend foundation: FastAPI application wiring, configuration, logging, project structure, containerization, storage directories, and the universal document domain model layer.

No AI logic, resume parsing, authentication, or database persistence models are implemented yet.

## Requirements

- Python 3.12+
- uv
- Docker and Docker Compose for containerized execution

## Install uv

Install uv with the official installer:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

On macOS or Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Project Setup

Create a local environment file:

```bash
cp .env.example .env
```

Install dependencies:

```bash
uv sync --group dev
```

Run the application locally:

```bash
uv run uvicorn app.main:app --app-dir backend --reload
```

Open the health endpoint:

```bash
curl http://localhost:8000/health
```

Upload a resume document:

```bash
curl -X POST http://localhost:8000/api/v1/upload/resume \
  -F "file=@resume.pdf;type=application/pdf"
```

## Docker

Create a local environment file before starting the stack:

```bash
cp .env.example .env
```

Build and run the backend with PostgreSQL:

```bash
docker compose up --build
```

The backend will be available at:

- `http://localhost:8000/health`
- `http://localhost:8000/api/v1/health`

## Directory Structure

```text
backend/
  app/
    api/                  HTTP API routes
    application/          Application layer, use cases, interfaces, and DTOs
    agents/               Future modular agent implementations
    core/                 Settings, logging, and constants
    domain/               Domain entities, repository contracts, and services
    infrastructure/       External adapters for database, storage, parsers, LLMs, and embeddings
    schemas/              API request and response schemas
    services/             Cross-cutting service modules
    utils/                Shared utilities
tests/                    Automated tests
storage/
  uploads/                Uploaded resumes and job files
  generated/              Generated reports and resume artifacts
logs/                     Application logs
```

## Quality Commands

```bash
uv run ruff check .
uv run black --check .
uv run mypy backend
uv run pytest
```

## Expected Health Response

```json
{
  "status": "healthy",
  "application": "AI Resume Intelligence Platform",
  "version": "0.1.0",
  "environment": "development"
}
```

## Expected Upload Response

```json
{
  "file_id": "9d69d74d-0000-4000-8000-000000000000",
  "filename": "resume.pdf",
  "size": 1024,
  "checksum": "sha256-hex-value",
  "status": "uploaded"
}
```

The API never returns filesystem paths. Uploaded files are stored with UUID filenames under the configured upload directories.

## Storage Configuration

Storage settings are loaded from environment variables:

- `RESUME_UPLOAD_DIR`
- `JOB_UPLOAD_DIR`
- `MAX_UPLOAD_SIZE_BYTES`
- `ALLOWED_UPLOAD_EXTENSIONS`
- `ALLOWED_UPLOAD_MIME_TYPES`

The default accepted document types are PDF and DOCX.

## Document Intelligence Subsystem

The Document Intelligence subsystem parses uploaded documents and converts them into a unified structural representation called the **Canonical Intermediate Representation (CIR)**.

### Pipeline Architecture

```text
Input Document (PDF/DOCX bytes)
  │
  ▼
1. Document Reader (PdfReader / DocxReader)
  │  (Layout Extraction & Page Splitting)
  ▼
DocumentContent (Unified Raw Text & TextBlocks)
  │
  ▼
2. Heading Detection (Heuristic Rules: Length, Caps, Standalone, Keywords)
  │  (Finds HeadingCandidate objects)
  ▼
3. Boundary Detection (Rules: NextHeading, EndOfDocument, PageBreak, Spacing)
  │  (Finds SectionBoundary coordinate segments)
  ▼
4. Section Detection & Classification (SectionMapper)
  │  (Determines SectionType and builds DocumentSections)
  ▼
5. CIR Builder (Validation & Statistics generation)
  │
  ▼
CanonicalIntermediateRepresentation (Immutable CIR)
```

### Components

- **DocumentReader**: Normalizes PDF layouts (using PyMuPDF dict coordinates) and DOCX files (python-docx paragraph streams) into `DocumentContent`.
- **HeadingDetector**: Scores candidate headings using heuristic criteria (length, casing, missing sentence punctuation, keyword dictionary matches, and positioning).
- **BoundaryDetector**: Maps headings to their respective physical bounds sequentially across pages and block ranges.
- **SectionDetectorService / SectionMapper**: Normalizes headings and maps them to standard categorized domain section types (e.g. `SectionType.EDUCATION`, `SectionType.EXPERIENCE`, `SectionType.SKILLS`, or `SectionType.OTHER` as fallback).
- **CIRBuilder**: Assembles, validates, calculates file statistics (characters, words, page count, average section size), and outputs the immutable CIR.
- **DocumentPipeline**: Coordinates all processing stages end-to-end, validating intermediate states, recording telemetry (durations), compiling pipeline warnings, and returning structured `PipelineResult` payloads.

