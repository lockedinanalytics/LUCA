from __future__ import annotations

from luca.intelligence.nfl.context.models import NflCoachingInput, NflCoachingOutput


def score_nfl_coaching(row: NflCoachingInput) -> NflCoachingOutput:
    warnings: list[str] = []

    aggression = row.fourth_down_aggression_score * 0.45 + row.two_point_strategy_score * 0.25 + row.personnel_grouping_edge_score * 0.30
    late_game = row.clock_management_score * 0.44 + row.challenge_efficiency_score * 0.22 + row.two_point_strategy_score * 0.14 + row.halftime_adjustment_score * 0.20
    red_zone = row.red_zone_play_call_score * 0.55 + row.run_pass_adaptability_score * 0.25 + row.personnel_grouping_edge_score * 0.20
    adjustment = row.halftime_adjustment_score * 0.36 + row.coordinator_matchup_score * 0.34 + row.run_pass_adaptability_score * 0.30

    if row.clock_management_score < 42:
        warnings.append("Clock management weakness detected.")
    if row.fourth_down_aggression_score >= 62:
        warnings.append("Aggressive fourth-down profile can raise scoring volatility.")

    final = aggression * 0.24 + late_game * 0.26 + red_zone * 0.24 + adjustment * 0.26

    return NflCoachingOutput(
        aggressiveness_score=round(max(0, min(100, aggression)), 2),
        late_game_management_score=round(max(0, min(100, late_game)), 2),
        red_zone_management_score=round(max(0, min(100, red_zone)), 2),
        adjustment_score=round(max(0, min(100, adjustment)), 2),
        final_coaching_score=round(max(0, min(100, final)), 2),
        warnings=warnings,
    )
