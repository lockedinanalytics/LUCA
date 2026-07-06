from __future__ import annotations

from pydantic import BaseModel

from luca.core.models import LucaRunResult


class BacktestSummary(BaseModel):
    slates: int
    games_evaluated: int
    recommendations: int
    avg_data_completeness: float
    notes: list[str]


def summarize_backtest(runs: list[LucaRunResult]) -> BacktestSummary:
    slates = len(runs)
    games = sum(row.games_evaluated for row in runs)
    recs = sum(len(row.recommendations) for row in runs)
    completeness = sum(row.data_completeness for row in runs) / slates if slates else 0.0
    return BacktestSummary(
        slates=slates,
        games_evaluated=games,
        recommendations=recs,
        avg_data_completeness=round(completeness, 3),
        notes=["Backtest summary shell. Phase 6 should add ROI, CLV, and calibration replay metrics."],
    )
