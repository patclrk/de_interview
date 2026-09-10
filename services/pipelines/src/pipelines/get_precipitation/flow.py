from db.models import PrecipitationReading
from prefect import flow

from pipelines.common import run_weather_flow


@flow(log_prints=True)
def get_precipitation() -> None:
    run_weather_flow(
        endpoint="precipitation",
        value_column="precipitation",
        model=PrecipitationReading,
    )
