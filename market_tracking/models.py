from __future__ import annotations

from pydantic import BaseModel


class MarketSnapshot(BaseModel):
    game_id: str
    market: str
    selection: str
    odds: float | None = None
    point: float | None = None
    book: str | None = None
    timestamp: str | None = None
