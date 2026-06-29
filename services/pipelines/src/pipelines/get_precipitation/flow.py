import os
import tomllib
from datetime import datetime, timezone
from pathlib import Path

import httpx
import polars as pl
from db.models import PrecipitationReading
from prefect import flow, get_run_logger, task
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import Session

_config_path = Path(__file__).parent / "config" / "config.toml"
with _config_path.open("rb") as _f:
    _config = tomllib.load(_f)


def _require_env(var: str) -> str:
    value = os.environ.get(var)
    if not value:
        raise EnvironmentError(f"Required environment variable '{var}' is not set")
    return value


API_URL = _require_env(_config["api"]["url_env"])
DATABASE_URL = _require_env(_config["database"]["url_env"])

@task(retries=3, retry_delay_seconds=5)
def extract_precipitation() -> dict[str, float]:
    logger = get_run_logger()

    with httpx.Client(timeout=10.0) as client:
        response = client.post(f"{API_URL}/precipitation", json={})
        response.raise_for_status()

    readings = response.json()["readings"]
    logger.info(f"Fetched precipitation readings: {readings}")
    return readings

@task
def transform_precipitation(readings: dict[str, float]) -> pl.DataFrame:
    df = pl.DataFrame(
        {
            "city": list(readings.keys()),
            "precipitation": list(readings.values()),
        }
    ).with_columns(pl.lit(datetime.now(timezone.utc)).alias("recorded_at"))

    return df

@task
def load_precipitation(df: pl.DataFrame, flow_run_id: str) -> int:
    engine = create_engine(DATABASE_URL)

    rows = df.with_columns(
        pl.lit(flow_run_id).alias("flow_run_id")
    ).to_dicts()

    with Session(engine) as session:
        session.execute(insert(PrecipitationReading), rows)
        session.commit()

    engine.dispose()
    return len(rows)

@flow(log_prints=True)
def get_precipitation() -> None:
    from prefect.runtime import flow_run

    readings = extract_precipitation()
    df = transform_precipitation(readings)
    load_precipitation(df, str(flow_run.id))