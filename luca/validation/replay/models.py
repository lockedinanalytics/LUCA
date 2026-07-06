from __future__ import annotations

from pydantic import BaseModel, Field


class HistoricalDecision(BaseModel):
    decision_id: str
    date: str
    sport: str
    league: str
    game_id: str
    market: str
    category: str
    selection: str
    odds: float | None = None
    units: float = 0.0
    confidence: float = 0.0
    projected_probability: float | None = None
    luca_score: float | None = None
    result: str | None = None
    units_won_lost: float | None = None
    closing_odds: float | None = None
    module_snapshot: dict[str, float] = Field(default_factory=dict)


class ReplayBatch(BaseModel):
    replay_id: str
    model_version: str
    decisions: list[HistoricalDecision] = Field(default_factory=list)


class ReplaySummary(BaseModel):
    replay_id: str
    model_version: str
    decisions: int
    graded_decisions: int
    wins: int
    losses: int
    pushes: int
    units: float
    roi: float | None
    notes: list[str] = Field(default_factory=list)
