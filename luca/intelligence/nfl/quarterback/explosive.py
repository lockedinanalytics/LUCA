from __future__ import annotations

from luca.intelligence.nfl.quarterback.models import NflQuarterbackExplosiveInput


def score_qb_explosive(row: NflQuarterbackExplosiveInput) -> tuple[float, list[str]]:
    warnings: list[str] = []
    score = 50.0

    if row.explosive_pass_rate is not None:
        score += (row.explosive_pass_rate - 12.0) * 1.2
    if row.air_yards_per_attempt is not None:
        score += (row.air_yards_per_attempt - 7.6) * 2.2
    if row.big_time_throw_rate is not None:
        score += (row.big_time_throw_rate - 4.0) * 3.2
    if row.deep_ball_accuracy_score is not None:
        score = score * 0.75 + row.deep_ball_accuracy_score * 0.25
    if row.yards_after_catch_creation_score is not None:
        score = score * 0.85 + row.yards_after_catch_creation_score * 0.15

    if row.explosive_pass_rate is not None and row.explosive_pass_rate < 9:
        warnings.append("Explosive pass rate is suppressed.")
    if row.air_yards_per_attempt is not None and row.air_yards_per_attempt < 6.2:
        warnings.append("Low air-yards profile limits ceiling.")

    return round(max(0, min(100, score)), 2), warnings
