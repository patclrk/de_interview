import random
from typing import Optional

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

router = APIRouter()

ALL_CITIES = ["Durham", "Raleigh", "Asheville", "Charlotte"]


class PrecipitationRequest(BaseModel):
    cities: Optional[list[str]] = None


class PrecipitationResponse(BaseModel):
    readings: dict[str, float]


@router.post("/precipitation")
def precipitation_readings(request: PrecipitationRequest):
    if random.random() < 0.05:
        return JSONResponse(
            status_code=500, content={"detail": "Internal Server Error"}
        )
    cities = request.cities if request.cities else ALL_CITIES
    readings = {city: round(random.uniform(0.0, 2.5), 2) for city in cities}
    return PrecipitationResponse(readings=readings)
