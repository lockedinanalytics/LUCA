from __future__ import annotations

from pydantic import BaseModel


class RunCreationInput(BaseModel):
    lineup_count: int = 9
    top_order_score: float = 55.0
    bottom_order_score: float = 50.0
    pitcher_matchup_score: float = 50.0
    weather_total_adjustment: float = 0.0
    park_factor: float = 1.0


class RunCreationOutput(BaseModel):
    projected_runs: float
    rcp_score: float
    notes: list[str]


def calculate_rcp(row: RunCreationInput) -> RunCreationOutput:
    notes = []
    lineup_penalty = 0 if row.lineup_count >= 9 else (9 - row.lineup_count) * 0.12
    base_runs = 4.25
    quality = (row.top_order_score * 0.45 + row.bottom_order_score * 0.25 + row.pitcher_matchup_score * 0.30 - 50) / 50
    runs = (base_runs * (1 + quality * 0.22) * row.park_factor) + row.weather_total_adjustment - lineup_penalty
    if row.lineup_count < 9:
        notes.append("Lineup incomplete; projection penalized.")
    score = max(0, min(100, 50 + (runs - 4.25) * 8))
    return RunCreationOutput(projected_runs=round(max(0, runs), 3), rcp_score=round(score, 2), notes=notes)
