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
│       ├── infrastructure/
│       │   └── storage/
│       │       ├── exceptions.py
│       │       ├── interfaces.py
│       │       ├── models.py
│       │       ├── provider.py
│       │       ├── storage_service.py
│       │       └── validator.py
│       └── main.py
├── tests/
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
