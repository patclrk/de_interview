# Data Engineering Interview
This repository was created as a brief take home coding assessment. It features some of the same technologies we use every day at work, and consists of several components:
- REST API that returns sample "weather" information
- [Prefect](https://docs.prefect.io/v3/get-started) Server and Worker (and its associated application database) that extracts data from the REST API
- Postgres Database that serves as a data warehouse with migrations managed via [alembic](https://alembic.sqlalchemy.org/en/latest/)

The project is intended to be run on your local machine only.

Take a moment to familiarize yourself with the project structure and code. Once you're comfortable, please complete the task described in the [Your Task](#your-task) section.

The instructions in the [Quickstart](#quickstart) section are accurate but they are also **incomplete**: sometimes we encounter source systems and libraries in the real world that aren't documented well (yes, we've been guilty of this too). In those situations we have to figure out how these systems work by exploring and testing the code ourselves. AI is a great tool for tasks like this and we encourage you to use it!

If you run into errors while working on the task please try to troubleshoot them first. Again, we highly recommend AI assistance here. If you are still stuck, please reach out to your hiring manager with any questions you may have.

Finally, your time is valuable. We greatly appreciate you dedicating some of it to completing this assessment and interviewing with our team.

Good luck and have fun!

## Quickstart
Run the following from your terminal:
```bash
docker compose up
```
- Prefect Server URL: http://localhost:4200

## Your Task
Please create a Prefect Flow that extracts data from the `/precipitation` endpoint and loads it into a new table in the Postgres `weather` database. Similar to the `get_temperatures` Flow, this Flow should run every 5 minutes. 

Unfortunately, getting "precipitation" data is not as reliable as getting "temperature" data: a random chance of receiving an HTTP 500 response has been added to this endpoint to simulate faulty network connectivity. You'll want to think of ways to make this Flow a bit more reliable (Hint: don't go overboard here).

When you complete the task please open a pull request in GitHub. During your interview we will walk through your code together.

#### Notes:
- Please do not modify any code in the `/services/api/` directory.
- We do not anticipate this task will take more than 2 hours.
- Please be thorough but avoid complexity when developing your solution.
- We care less about the code itself and more about the design decisions you, the human, make.
- AI use is encouraged!
- Exclamation points are also encouraged!
- If you can familiarize yourself with new projects and produce simple and effective solutions relatively quickly, we think you'll do really well on our team.

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

