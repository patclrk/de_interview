from db.models import TemperatureReading
from prefect import flow

from pipelines.common import run_weather_flow


@flow(log_prints=True)
def get_temperatures() -> None:
    run_weather_flow(
        endpoint="temperature",
        value_column="temperature_f",
        model=TemperatureReading,
    )
