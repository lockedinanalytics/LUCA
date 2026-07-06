from __future__ import annotations

from luca.intelligence.nfl.context.models import NflSituationalInput, NflSituationalOutput


def score_nfl_situational(row: NflSituationalInput) -> NflSituationalOutput:
    warnings: list[str] = []

    rest_edge = 50.0
    if row.rest_days is not None and row.opponent_rest_days is not None:
        rest_edge += (row.rest_days - row.opponent_rest_days) * 3.0
    if row.short_week:
        rest_edge -= 8
        warnings.append("Short-week penalty applied.")
    if row.off_bye:
        rest_edge += 8
    if row.opponent_off_bye:
        rest_edge -= 6

    travel = 60.0
    travel -= min(18, row.miles_traveled / 160.0)
    travel -= min(12, abs(row.time_zone_shift) * 3.0)
    if row.international_travel:
        travel -= 10
        warnings.append("International travel risk detected.")

    motivation = row.revenge_spot_score * 0.35 + (100 - row.lookahead_risk_score) * 0.25 + 50.0 * 0.40
    if row.divisional_game:
        motivation += 3
        warnings.append("Divisional familiarity increases variance.")

    pace_script = row.pace_tendency_score * 0.45 + row.game_script_stability_score * 0.55

    final = rest_edge * 0.30 + travel * 0.25 + motivation * 0.20 + pace_script * 0.25

    return NflSituationalOutput(
        rest_edge_score=round(max(0, min(100, rest_edge)), 2),
        travel_score=round(max(0, min(100, travel)), 2),
        motivation_score=round(max(0, min(100, motivation)), 2),
        pace_script_score=round(max(0, min(100, pace_script)), 2),
        final_situational_score=round(max(0, min(100, final)), 2),
        warnings=warnings,
    )
