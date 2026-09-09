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

_config_path = Path(__file__).parents[1] / "config" / "config.toml"
with _config_path.open("rb") as _f:
    _config = tomllib.load(_f)


def _require_env(var: str) -> str:
    value = os.environ.get(var)
    if not value:
        raise EnvironmentError(f"Required environment variable '{var}' is not set")
    return value


API_URL = _require_env(_config["api"]["url_env"])
DATABASE_URL = _require_env(_config["database"]["url_env"])


# ~5% of calls return HTTP 500. Transient and stateless, so retries are the fix!
# Retrying only extract means a successful load never re-runs — no duplicate rows.
@task(retries=3, retry_delay_seconds=[5, 15, 30])
def extract() -> dict[str, float]:
    logger = get_run_logger()
    with httpx.Client(timeout=10.0) as client:  # timeout guards a hung connection...
        response = client.post(f"{API_URL}/precipitation", json={})
        response.raise_for_status()  # turns the 500 into a retryable exception!
    readings: dict[str, float] = response.json()["readings"]
    logger.info(f"Fetched {len(readings)} precipitation readings: {readings}")
    return readings


@task
def transform(readings: dict[str, float]) -> pl.DataFrame:
    logger = get_run_logger()
    df = pl.DataFrame(
        {
            "city": list(readings.keys()),
            "precipitation": list(readings.values()),
        }
    ).with_columns(pl.lit(datetime.now(timezone.utc)).alias("recorded_at"))
    logger.info(f"Transformed {len(df)} readings into DataFrame")
    return df


@task
def load(df: pl.DataFrame, flow_run_id: str) -> int:
    logger = get_run_logger()
    engine = create_engine(DATABASE_URL)
    rows = df.with_columns(pl.lit(flow_run_id).alias("flow_run_id")).to_dicts()
    with Session(engine) as session:
        session.execute(insert(PrecipitationReading), rows)
        session.commit()
    engine.dispose()
    logger.info(f"Wrote {len(rows)} records to dw_weather.precipitation_readings")
    return len(rows)


@flow(log_prints=True)
def get_precipitation() -> None:
    logger = get_run_logger()
    from prefect.runtime import flow_run

    readings = extract()
    df = transform(readings)
    load(df, str(flow_run.id))  # stamps every row with its run, for lineage!
    logger.info("Flow complete.")
