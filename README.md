# Data Engineering Interview

## Quickstart
Run the following from your terminal:
```bash
docker compose up
```
- Prefect Server URL: http://localhost:4200

## Your Task
Please create a Prefect Flow that extracts data from the `/precipitation` endpoint and loads it into the postgres `weather` database. Unfortunately, getting precipitation data is not as reliable as temperature data! Please open a merge request when you have completed the task and we'll review your code together during your interview. If you have any questions while you are working please do not hesitate to reach out!

#### Notes:
- Please do not modify any code in the `/services/api` directory.
- AI assistance is encouraged! We care less about the code itself and more about the design choices you make and the prompts you write. We'd love to talk about your personal AI workflow and tool choices during your interview.
- We do not anticipate this task will take more than 2 hours. Please be thorough but recommend simplicty when developing your solution.

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

