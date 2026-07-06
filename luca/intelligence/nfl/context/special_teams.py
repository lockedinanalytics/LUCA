from __future__ import annotations

from luca.intelligence.nfl.context.models import NflSpecialTeamsInput, NflSpecialTeamsOutput


def score_nfl_special_teams(row: NflSpecialTeamsInput) -> NflSpecialTeamsOutput:
    warnings: list[str] = []

    kicking = row.kicker_consistency_score * 0.38 + row.long_fg_score * 0.22 + row.weather_adjusted_kicking_score * 0.40
    field_position = row.punter_field_position_score * 0.55 + row.coverage_unit_score * 0.25 + row.hidden_yardage_score * 0.20
    returns = row.kickoff_return_score * 0.34 + row.punt_return_score * 0.34 + row.hidden_yardage_score * 0.32
    coverage_pressure = row.coverage_unit_score * 0.45 + row.block_pressure_score * 0.25 + row.hidden_yardage_score * 0.30

    if row.weather_adjusted_kicking_score < 43:
        warnings.append("Weather-adjusted kicking risk detected.")
    if row.hidden_yardage_score >= 60:
        warnings.append("Special teams hidden-yardage edge present.")

    final = kicking * 0.30 + field_position * 0.28 + returns * 0.18 + coverage_pressure * 0.24

    return NflSpecialTeamsOutput(
        kicking_score=round(max(0, min(100, kicking)), 2),
        field_position_score=round(max(0, min(100, field_position)), 2),
        return_game_score=round(max(0, min(100, returns)), 2),
        coverage_pressure_score=round(max(0, min(100, coverage_pressure)), 2),
        final_special_teams_score=round(max(0, min(100, final)), 2),
        warnings=warnings,
    )
