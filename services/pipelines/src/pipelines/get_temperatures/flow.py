import os
import tomllib
from datetime import datetime, timezone
from pathlib import Path

import httpx
import polars as pl
from db.models import TemperatureReading
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


@task
def extract() -> dict[str, float]:
    logger = get_run_logger()
    with httpx.Client() as client:
        response = client.post(f"{API_URL}/temperature", json={})
        response.raise_for_status()
    readings: dict[str, float] = response.json()["readings"]
    logger.info(f"Fetched {len(readings)} temperature readings: {readings}")
    return readings


@task
def transform(readings: dict[str, float]) -> pl.DataFrame:
    logger = get_run_logger()
    df = pl.DataFrame(
        {
            "city": list(readings.keys()),
            "temperature_f": list(readings.values()),
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
        session.execute(insert(TemperatureReading), rows)
        session.commit()
    engine.dispose()
    logger.info(f"Wrote {len(rows)} records to dw_weather.temperature_readings")
    return len(rows)


@flow(log_prints=True)
def get_temperatures() -> None:
    logger = get_run_logger()
    from prefect.runtime import flow_run

    readings = extract()
    df = transform(readings)
    load(df, str(flow_run.id))
    logger.info("Flow complete.")
