import random
from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

ALL_CITIES = ["Durham", "Raleigh", "Asheville", "Charlotte"]


class TemperatureRequest(BaseModel):
    cities: Optional[list[str]] = None


class TemperatureResponse(BaseModel):
    readings: dict[str, float]


@router.post("/temperature")
def temperature_readings(request: TemperatureRequest) -> TemperatureResponse:
    cities = request.cities if request.cities else ALL_CITIES
    readings = {city: round(random.uniform(70.0, 80.0), 1) for city in cities}
    return TemperatureResponse(readings=readings)
