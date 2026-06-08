# de_interview
Data Engineering Interview

## Repository Structure

```
de_interview/
├── docker-compose.yml        # Orchestrates all services
├── pyproject.toml            # uv workspace root
├── uv.lock                   # Pinned dependency lockfile
├── .env                      # Local environment variables (not committed)
├── .env.example              # Template for .env
│
├── packages/
│   └── db/                   # SQLAlchemy models & Alembic migrations
│       ├── src/db/
│       │   └── models.py     # ORM models
│       └── migrations/       # Alembic migration scripts
│
└── services/
    ├── api/                  # FastAPI service
    │   ├── src/api/
    │   │   ├── main.py
    │   │   └── routers/
    │   │       └── temperature.py
    │   └── tests/
    │       └── test_api.py
    │
    └── pipelines/            # Data pipelines
        ├── prefect.yaml      # Deployment definitions
        ├── entrypoint.sh     # Prefect Worker startup script
        └── src/pipelines/
            └── get_temperatures/   # example ETL
                ├── flow.py
                └── config/
                    └── config.toml # Default API and database URLs
```

