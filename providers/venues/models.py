from __future__ import annotations

from pydantic import BaseModel


class VenueLocation(BaseModel):
    name: str
    team: str | None = None
    latitude: float
    longitude: float
    roof: str = "unknown"
    altitude_ft: float | None = None
