from __future__ import annotations

from pydantic import BaseModel


class WeatherSnapshot(BaseModel):
    game_id: str
    available: bool
    temperature_f: float | None = None
    wind_speed_mph: float | None = None
    wind_direction_degrees: float | None = None
    precipitation_probability: float | None = None
    humidity: float | None = None
    source: str = "unknown"
    warnings: list[str] = []


class WeatherImpact(BaseModel):
    weather_score: float
    wind_run_multiplier: float
    total_adjustment: float
    risk: str
    notes: list[str]
