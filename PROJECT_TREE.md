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
│       │   │   ├── cir_builder.py            # [TICKET-005.5] CIR builder and validator
│       │   │   ├── cir_statistics.py         # [TICKET-005.5] CIR statistics application model
│       │   │   ├── document_pipeline.py      # [TICKET-005.6] End-to-end integration pipeline
│       │   │   ├── heading_candidate.py      # Heading candidate model
│       │   │   ├── heading_detector.py       # Heading detection service orchestrator
│       │   │   ├── heading_rules.py          # Scoring heuristics engine
│       │   │   ├── pipeline_result.py        # [TICKET-005.6] Pipeline execution result model
│       │   │   ├── pipeline_validator.py     # [TICKET-005.6] Stage execution validator
│       │   │   ├── section_boundary.py       # [TICKET-005.3] Section boundary model
│       │   │   ├── section_detector.py       # [TICKET-005.4] Section detector Protocol
│       │   │   ├── section_detector_service.py # [TICKET-005.4] Section detector service
│       │   │   └── section_mapper.py         # [TICKET-005.4] Section heading classification mapper
│       │   ├── resume_builder/               # [TASK-006] Resume intelligence builder
│       │   │   ├── candidate_builder.py      # [TICKET-006.1] Candidate domain entity builder
│       │   │   ├── candidate_mapper.py       # [TICKET-006.1] Candidate properties extractor/mapper
│       │   │   ├── candidate_validator.py    # [TICKET-006.1] Candidate fields validator
│       │   │   ├── education_builder.py      # [TICKET-006.2] Education domain entity builder
│       │   │   ├── education_mapper.py       # [TICKET-006.2] Education parser/mapper
│       │   │   ├── education_validator.py    # [TICKET-006.2] Education fields validator
│       │   │   ├── experience_builder.py     # [TICKET-006.3] Experience domain entity builder
│       │   │   ├── experience_mapper.py      # [TICKET-006.3] Experience parser/mapper
│       │   │   └── experience_validator.py   # [TICKET-006.3] Experience fields validator
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
│       │       ├── canonical_intermediate_representation.py # [TICKET-005.5] CIR domain entity
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
│   ├── test_candidate_builder.py             # [TICKET-006.1] Candidate builder tests
│   ├── test_cir_builder.py                   # [TICKET-005.5] CIR builder tests
│   ├── test_document_entities.py
│   ├── test_document_intelligence.py         # [TASK-004] 32 pipeline tests
│   ├── test_document_pipeline.py             # [TICKET-005.6] Document pipeline integration tests
│   ├── test_education_builder.py             # [TICKET-006.2] Education builder tests
│   ├── test_experience_builder.py            # [TICKET-006.3] Experience builder tests
│   ├── test_heading_detection.py             # [TICKET-005.2] Heading detection tests
│   ├── test_section_detection.py             # [TICKET-005.4] Section detection tests
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
