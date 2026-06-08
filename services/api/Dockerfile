FROM python:3.14-slim

WORKDIR /app

RUN pip install --no-cache-dir uv

# Copy workspace root config and lockfile
COPY pyproject.toml uv.lock /app/

# Copy workspace members needed by the api package
COPY packages/db /app/packages/db
COPY services/api /app/services/api

# Install api and all its dependencies from the lockfile
RUN uv sync --frozen --package api

# Put the venv on PATH
ENV PATH="/app/.venv/bin:$PATH"

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
