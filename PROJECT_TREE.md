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
│       │   ├── document_analysis/            # [TICKET-005.2] Heading & section analysis
│       │   │   ├── boundary_detector.py      # [TICKET-005.3] Boundary detection orchestrator
│       │   │   ├── boundary_rules.py         # [TICKET-005.3] Boundary heuristics engine
│       │   │   ├── heading_candidate.py      # Heading candidate model
│       │   │   ├── heading_detector.py       # Heading detection service orchestrator
│       │   │   ├── heading_rules.py          # Scoring heuristics engine
│       │   │   └── section_boundary.py       # [TICKET-005.3] Section boundary model
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
│       │       ├── document_section.py       # [TICKET-005.1] Document section domain entity
│       │       ├── evidence.py
│       │       ├── job_description.py
│       │       ├── page.py                   # [TASK-004] Structured page entity
│       │       ├── recommendation.py
│       │       ├── resume.py
│       │       ├── section_type.py           # [TICKET-005.1] Section type StrEnum
│       │       ├── structured_document.py    # [TICKET-005.1] Structured document domain entity
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
│   ├── test_boundary_detection.py            # [TICKET-005.3] Section boundary detection tests
│   ├── test_document_entities.py
│   ├── test_document_intelligence.py         # [TASK-004] 32 pipeline tests
│   ├── test_heading_detection.py             # [TICKET-005.2] Heading detection tests
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
