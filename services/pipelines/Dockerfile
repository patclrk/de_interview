FROM prefecthq/prefect:3-python3.14

WORKDIR /app

RUN pip install --no-cache-dir uv

# Copy workspace root config and lockfile
COPY pyproject.toml uv.lock /app/

# Copy workspace members needed by the pipelines package
COPY packages/db /app/packages/db
COPY services/pipelines /app/services/pipelines

# Install pipelines and all its dependencies from the lockfile
RUN uv sync --frozen --package pipelines

# Make pipeline source importable and put the venv on PATH
ENV PYTHONPATH=/app/services/pipelines/src
ENV PATH="/app/.venv/bin:$PATH"

COPY services/pipelines/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
