from fastapi import FastAPI

from api.routers import precipitation, temperature

app = FastAPI(title="Weather API", version="0.1.0")

app.include_router(temperature.router)
app.include_router(precipitation.router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
