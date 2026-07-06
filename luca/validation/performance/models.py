from __future__ import annotations

from pydantic import BaseModel


class PerformanceSlice(BaseModel):
    key: str
    decisions: int
    wins: int
    losses: int
    pushes: int
    units: float
    risked: float
    roi: float | None
    win_rate: float | None


class PerformanceReport(BaseModel):
    by_category: list[PerformanceSlice]
    by_market: list[PerformanceSlice]
    by_sport: list[PerformanceSlice]
    by_league: list[PerformanceSlice]
