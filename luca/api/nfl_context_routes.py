from __future__ import annotations

from fastapi import APIRouter

from luca.intelligence.nfl.context.coaching import score_nfl_coaching
from luca.intelligence.nfl.context.engine import calculate_nfl_context
from luca.intelligence.nfl.context.environment import score_nfl_environment
from luca.intelligence.nfl.context.models import NflCoachingInput, NflContextInput, NflEnvironmentInput, NflSituationalInput, NflSpecialTeamsInput
from luca.intelligence.nfl.context.situational import score_nfl_situational
from luca.intelligence.nfl.context.special_teams import score_nfl_special_teams

router = APIRouter(prefix="/intelligence/nfl/context", tags=["nfl-context"])


@router.get("/situational/sample")
async def situational_sample():
    return score_nfl_situational(NflSituationalInput(rest_days=7, opponent_rest_days=6, miles_traveled=900, time_zone_shift=1, divisional_game=True, revenge_spot_score=56, lookahead_risk_score=44, pace_tendency_score=58, game_script_stability_score=57)).model_dump()


@router.get("/coaching/sample")
async def coaching_sample():
    return score_nfl_coaching(NflCoachingInput(fourth_down_aggression_score=60, two_point_strategy_score=56, red_zone_play_call_score=58, run_pass_adaptability_score=57, clock_management_score=55, challenge_efficiency_score=53, halftime_adjustment_score=59, coordinator_matchup_score=58, personnel_grouping_edge_score=57)).model_dump()


@router.get("/special-teams/sample")
async def special_teams_sample():
    return score_nfl_special_teams(NflSpecialTeamsInput(kicker_consistency_score=58, long_fg_score=56, weather_adjusted_kicking_score=55, punter_field_position_score=59, kickoff_return_score=54, punt_return_score=57, coverage_unit_score=58, block_pressure_score=53, hidden_yardage_score=60)).model_dump()


@router.get("/environment/sample")
async def environment_sample():
    return score_nfl_environment(NflEnvironmentInput(wind_mph=12, precipitation_score=54, snow_score=60, temperature_f=42, humidity_pct=65, elevation_ft=520, roof_state="open", surface_score=55, weather_severity_score=48)).model_dump()


@router.get("/context-v2/sample")
async def context_v2_sample():
    return calculate_nfl_context(NflContextInput(
        situational=NflSituationalInput(rest_days=7, opponent_rest_days=6, miles_traveled=900, time_zone_shift=1, divisional_game=True, revenge_spot_score=56, lookahead_risk_score=44, pace_tendency_score=58, game_script_stability_score=57),
        coaching=NflCoachingInput(fourth_down_aggression_score=60, two_point_strategy_score=56, red_zone_play_call_score=58, run_pass_adaptability_score=57, clock_management_score=55, challenge_efficiency_score=53, halftime_adjustment_score=59, coordinator_matchup_score=58, personnel_grouping_edge_score=57),
        special_teams=NflSpecialTeamsInput(kicker_consistency_score=58, long_fg_score=56, weather_adjusted_kicking_score=55, punter_field_position_score=59, kickoff_return_score=54, punt_return_score=57, coverage_unit_score=58, block_pressure_score=53, hidden_yardage_score=60),
        environment=NflEnvironmentInput(wind_mph=12, precipitation_score=54, snow_score=60, temperature_f=42, humidity_pct=65, elevation_ft=520, roof_state="open", surface_score=55, weather_severity_score=48),
    )).model_dump()
