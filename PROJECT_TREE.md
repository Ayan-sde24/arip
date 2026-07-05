# Project Tree

```text
.
├── backend/
│   └── app/
│       ├── api/
│       │   └── v1/
│       │       ├── health.py
│       │       └── upload.py
│       ├── application/
│       │   └── services/
│       │       └── document_storage.py
│       ├── core/
│       │   ├── config.py
│       │   ├── constants.py
│       │   └── logger.py
│       ├── domain/
│       │   └── entities/
│       │       ├── __init__.py
│       │       ├── agent_result.py
│       │       ├── analysis_context.py
│       │       ├── candidate.py
│       │       ├── document.py
│       │       ├── document_content.py       # [TASK-004] Unified document representation
│       │       ├── evidence.py
│       │       ├── job_description.py
│       │       ├── page.py                   # [TASK-004] Structured page entity
│       │       ├── recommendation.py
│       │       ├── resume.py
│       │       └── text_block.py             # [TASK-004] Text block with reading order
│       ├── infrastructure/
│       │   ├── parser/                       # [TASK-004] Document Intelligence Pipeline
│       │   │   ├── __init__.py
│       │   │   ├── document_content_builder.py
│       │   │   ├── document_reader.py        # Pipeline orchestrator (Stage 1→2→3)
│       │   │   ├── docx_reader.py
│       │   │   ├── exceptions.py
│       │   │   ├── interfaces.py
│       │   │   ├── layout_analyzer.py
│       │   │   ├── models.py
│       │   │   ├── pdf_reader.py
│       │   │   └── utils.py
│       │   └── storage/
│       │       ├── exceptions.py
│       │       ├── interfaces.py
│       │       ├── models.py
│       │       ├── provider.py
│       │       ├── storage_service.py
│       │       └── validator.py
│       └── main.py
├── tests/
│   ├── test_document_entities.py
│   ├── test_document_intelligence.py         # [TASK-004] 32 pipeline tests
│   └── test_storage_service.py
├── storage/
│   ├── generated/
│   └── uploads/
├── CHANGELOG.md
├── Dockerfile
├── PROJECT_TREE.md
├── README.md
├── docker-compose.yml
└── pyproject.toml
```
