from __future__ import annotations

from luca.intelligence.mlb.environment.models import UmpireProfileInput, UmpireProfileOutput


def score_umpire_profile(row: UmpireProfileInput) -> UmpireProfileOutput:
    warnings: list[str] = []

    zone = row.strike_zone_score * 0.45 + row.consistency_score * 0.25 + row.strikeout_rate_score * 0.30
    pitcher_support = row.pitcher_friendly_score * 0.45 + row.strikeout_rate_score * 0.25 + (100 - row.walk_rate_score) * 0.15 + row.consistency_score * 0.15
    run_env = row.over_under_tendency_score * 0.45 + row.walk_rate_score * 0.25 + (100 - row.pitcher_friendly_score) * 0.20 + row.home_road_bias_score * 0.10
    volatility = 100 - row.consistency_score

    if row.consistency_score < 43:
        warnings.append(f"{row.name}: low consistency profile increases variance.")
    if row.walk_rate_score >= 60:
        warnings.append(f"{row.name}: elevated walk tendency can lift run environment.")

    final = zone * 0.26 + pitcher_support * 0.26 + run_env * 0.26 + (100 - volatility) * 0.22

    return UmpireProfileOutput(
        zone_score=round(max(0, min(100, zone)), 2),
        run_environment_score=round(max(0, min(100, run_env)), 2),
        pitcher_support_score=round(max(0, min(100, pitcher_support)), 2),
        volatility_score=round(max(0, min(100, volatility)), 2),
        final_umpire_score=round(max(0, min(100, final)), 2),
        warnings=warnings,
    )
