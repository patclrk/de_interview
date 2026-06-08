#!/bin/bash
set -e

echo "Waiting for Prefect server at ${PREFECT_API_URL}..."
until python -c "
import urllib.request, sys, os
url = os.environ.get('PREFECT_API_URL', 'http://prefect-server:4200/api') + '/health'
try:
    urllib.request.urlopen(url, timeout=5)
    sys.exit(0)
except Exception:
    sys.exit(1)
" 2>/dev/null; do
    echo "  not ready — retrying in 3s..."
    sleep 3
done
echo "Prefect server is ready."

echo "Creating work pool 'default-pool' (type: process)..."
prefect work-pool create --type process default-pool || true

echo "Deploying pipelines from prefect.yaml..."
cd /app/services/pipelines
prefect deploy --all

echo "Starting worker..."
exec prefect worker start --pool default-pool
