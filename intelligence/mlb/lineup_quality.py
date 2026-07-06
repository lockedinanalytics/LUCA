from __future__ import annotations

from pydantic import BaseModel


class LineupQualityInput(BaseModel):
    lineup_count: int = 9
    top_four_xwoba_score: float = 50.0
    bottom_five_xwoba_score: float = 50.0
    platoon_advantage_score: float = 50.0
    strikeout_risk_score: float = 50.0
    power_score: float = 50.0


class LineupQualityOutput(BaseModel):
    depth_score: float
    run_creation_score: float
    volatility_score: float
    final_lineup_score: float
    notes: list[str]


def calculate_lineup_quality(row: LineupQualityInput) -> LineupQualityOutput:
    notes = []
    depth = row.top_four_xwoba_score * 0.55 + row.bottom_five_xwoba_score * 0.45
    if row.lineup_count < 9:
        depth -= (9 - row.lineup_count) * 3
        notes.append("Incomplete lineup penalty.")

    run_creation = (
        row.top_four_xwoba_score * 0.35
        + row.bottom_five_xwoba_score * 0.20
        + row.platoon_advantage_score * 0.20
        + row.power_score * 0.15
        + row.strikeout_risk_score * 0.10
    )
    volatility = 100 - abs(row.power_score - row.strikeout_risk_score)
    final = depth * 0.35 + run_creation * 0.50 + volatility * 0.15

    return LineupQualityOutput(
        depth_score=round(max(0, min(100, depth)), 2),
        run_creation_score=round(max(0, min(100, run_creation)), 2),
        volatility_score=round(max(0, min(100, volatility)), 2),
        final_lineup_score=round(max(0, min(100, final)), 2),
        notes=notes,
    )
