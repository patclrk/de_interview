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

with _config_path.open("rb") as f:
    _config = tomllib.load(f)   

def _require_env(var: str) -> str:
    value = os.getenv(var)
    if not value:
        raise ValueError(f"Environment variable '{var}' is not set")
    return value

API_URL = _require_env(_config["api"]["url_env"])
DATABASE_URL = _require_env(_config["database"]["url_env"])

@task(retries=3, retry_delay_seconds=10)
def extract() -> dict[str, float]:
    logger = get_run_logger()
    with httpx.Client() as client:
        response = client.post(f"{API_URL}/precipitation", json={})
        response.raise_for_status()
    readings: dict[str, float] = response.json()["readings"]
    logger.info(f"Fetched {len(readings)} precipitation readings: {readings}")
    return readings

@task
def transform(readings: dict[str, float]) -> pl.DataFrame:
    logger = get_run_logger()
    df = pl.DataFrame(
        {
            "city": list(readings.keys()),
            "precipitation_in": list(readings.values()),
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
    load(df, str(flow_run.id))
    logger.info("Flow complete.")


