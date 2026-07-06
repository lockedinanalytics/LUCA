from __future__ import annotations

from fastapi import APIRouter

from luca.intelligence.nfl.quarterback.engine import calculate_nfl_quarterback_intelligence
from luca.intelligence.nfl.quarterback.models import (
    NflQuarterbackDecisionInput,
    NflQuarterbackEfficiencyInput,
    NflQuarterbackExplosiveInput,
    NflQuarterbackIntelligenceInput,
    NflQuarterbackMatchupInput,
    NflQuarterbackMobilityInput,
    NflQuarterbackPressureInput,
    NflQuarterbackSituationalInput,
)

router = APIRouter(prefix="/intelligence/nfl/quarterback", tags=["nfl-quarterback"])


@router.get("/qb-v2/sample")
async def qb_v2_sample():
    return calculate_nfl_quarterback_intelligence(NflQuarterbackIntelligenceInput(
        efficiency=NflQuarterbackEfficiencyInput(epa_per_play=0.16, success_rate=48.5, cpoe=2.8, anya=7.4, third_down_success_rate=44.0, red_zone_efficiency=61.0),
        explosive=NflQuarterbackExplosiveInput(explosive_pass_rate=14.5, air_yards_per_attempt=8.3, big_time_throw_rate=5.6, deep_ball_accuracy_score=61, yards_after_catch_creation_score=57),
        pressure=NflQuarterbackPressureInput(pressure_epa_per_play=-0.08, pressure_to_sack_rate=17.5, blitz_epa_per_play=0.11, clean_pocket_epa_per_play=0.28, time_to_throw=2.72),
        decision=NflQuarterbackDecisionInput(turnover_worthy_play_rate=2.8, interception_rate=1.8, sack_avoidance_score=61, checkdown_efficiency_score=58, late_down_decision_score=60),
        mobility=NflQuarterbackMobilityInput(scramble_epa=0.18, designed_run_epa=0.05, pressure_escape_score=62, rushing_success_rate=46.0),
        situational=NflQuarterbackSituationalInput(two_minute_score=59, comeback_score=57, home_away_split_score=55, indoor_outdoor_split_score=56, weather_sensitivity_score=54, injury_penalty=0, fatigue_penalty=1),
        matchup=NflQuarterbackMatchupInput(opponent_pressure_score=56, opponent_coverage_score=54, opponent_blitz_rate_score=58, offensive_line_support_score=57, receiver_separation_score=59, coaching_pass_design_score=58),
    )).model_dump()
