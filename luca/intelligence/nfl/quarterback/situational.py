from __future__ import annotations

from luca.intelligence.nfl.quarterback.models import NflQuarterbackSituationalInput


def score_qb_situational(row: NflQuarterbackSituationalInput) -> tuple[float, list[str]]:
    warnings: list[str] = []
    score = 50.0

    for value, weight in [
        (row.two_minute_score, 0.18),
        (row.comeback_score, 0.14),
        (row.home_away_split_score, 0.12),
        (row.indoor_outdoor_split_score, 0.12),
        (row.weather_sensitivity_score, 0.18),
    ]:
        if value is not None:
            score = score * (1 - weight) + value * weight

    score -= row.injury_penalty
    score -= row.fatigue_penalty

    if row.injury_penalty >= 8:
        warnings.append("QB injury penalty materially affects projection.")
    if row.weather_sensitivity_score is not None and row.weather_sensitivity_score < 42:
        warnings.append("QB has adverse weather sensitivity.")

    return round(max(0, min(100, score)), 2), warnings
