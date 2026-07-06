from __future__ import annotations

from pydantic import BaseModel


class FeatureAttributionRow(BaseModel):
    feature: str
    decisions: int
    avg_score_wins: float | None
    avg_score_losses: float | None
    spread: float | None
    contribution_signal: str


class FeatureAttributionReport(BaseModel):
    rows: list[FeatureAttributionRow]
    warnings: list[str]
