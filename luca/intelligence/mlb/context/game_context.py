from __future__ import annotations

from luca.intelligence.mlb.environment.models import GameContextInput, GameContextOutput


def score_game_context(row: GameContextInput) -> GameContextOutput:
    warnings: list[str] = []

    rest = row.lineup_rest_risk_score
    motivation = row.motivation_score
    managerial = row.managerial_aggression_score

    if row.day_game_after_night:
        rest -= 8
        warnings.append("Day game after night game creates lineup rest risk.")
    if row.rubber_game:
        motivation += 4
        managerial += 3
    if row.elimination_or_clinch_context:
        motivation += 8
        managerial += 5
        warnings.append("High-leverage standings context.")

    if row.series_game_number is not None and row.series_game_number >= 3:
        managerial += 2

    final = rest * 0.35 + motivation * 0.35 + managerial * 0.30

    return GameContextOutput(
        rest_context_score=round(max(0, min(100, rest)), 2),
        motivation_context_score=round(max(0, min(100, motivation)), 2),
        managerial_context_score=round(max(0, min(100, managerial)), 2),
        final_context_score=round(max(0, min(100, final)), 2),
        warnings=warnings,
    )
