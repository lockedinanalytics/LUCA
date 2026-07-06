from __future__ import annotations

from pydantic import BaseModel


class MarketEvaluation(BaseModel):
    market: str
    selection: str
    projected_value: float | None = None
    market_value: float | None = None
    projected_probability: float | None = None
    implied_probability: float | None = None
    edge: float
    tier: str
    notes: list[str] = []
