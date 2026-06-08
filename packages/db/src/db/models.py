from sqlalchemy import Column, DateTime, Float, Integer, String, func
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class TemperatureReading(Base):
    __tablename__ = "temperature_readings"
    __table_args__ = {"schema": "dw_weather"}

    id = Column(Integer, primary_key=True)
    city = Column(String(100), nullable=False)
    temperature_f = Column(Float, nullable=False)
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())
    flow_run_id = Column(String(100), nullable=True)
