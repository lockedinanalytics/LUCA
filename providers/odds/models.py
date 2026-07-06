from __future__ import annotations

from typing import Any
from pydantic import BaseModel, Field

from luca.core.models import MarketLine


class OddsProviderStatus(BaseModel):
    provider: str
    configured: bool
    live_enabled: bool
    details: dict[str, Any] = Field(default_factory=dict)


class OddsEvent(BaseModel):
    provider_event_id: str
    sport_key: str
    commence_time: str | None = None
    home_team: str
    away_team: str
    market_lines: list[MarketLine] = Field(default_factory=list)
    raw: dict[str, Any] = Field(default_factory=dict)
