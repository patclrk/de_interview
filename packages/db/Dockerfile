FROM python:3.14-slim

WORKDIR /app

RUN pip install --no-cache-dir uv

# Copy workspace root config and lockfile
COPY pyproject.toml uv.lock /app/

# Copy workspace members needed by the db package
COPY packages/db /app/packages/db

# Install db and all its dependencies from the lockfile
RUN uv sync --frozen --package db

# Put the venv on PATH
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app/packages/db
CMD ["alembic", "upgrade", "head"]
