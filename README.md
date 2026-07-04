# ARIP Backend

ARIP is an enterprise AI Resume Intelligence Platform. This repository currently contains the initial backend foundation only: FastAPI application wiring, configuration, logging, project structure, containerization, and storage directories.

No AI logic, resume parsing, authentication, or database models are implemented in this foundation.

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
