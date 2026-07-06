from __future__ import annotations

from pydantic import BaseModel


class WeatherSnapshot(BaseModel):
    game_id: str
    available: bool
    temperature: float | None = None
    wind_speed: float | None = None
    wind_direction: float | None = None
    precipitation: float | None = None
    humidity: float | None = None
    source: str = "unknown"
