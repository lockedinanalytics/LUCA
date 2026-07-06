from __future__ import annotations

from fastapi import APIRouter

from luca.intelligence.mlb.defense.baserunning import score_baserunner_prevention
from luca.intelligence.mlb.defense.catcher import score_catcher
from luca.intelligence.mlb.defense.engine import calculate_defensive_intelligence
from luca.intelligence.mlb.defense.fielding import score_fielding_unit
from luca.intelligence.mlb.defense.models import (
    BaserunnerPreventionInput,
    CatcherInput,
    DefensiveIntelligenceInput,
    FieldingUnitInput,
)

router = APIRouter(prefix="/intelligence/mlb/defense", tags=["mlb-defense"])


@router.get("/catcher/sample")
async def catcher_sample():
    return score_catcher(CatcherInput(
        name="Catcher A",
        framing_score=62,
        blocking_score=58,
        throwing_score=56,
        pop_time_score=55,
        game_calling_score=60,
        pitcher_familiarity_score=64,
        workload_fatigue_score=57,
    )).model_dump()


@router.get("/fielding/sample")
async def fielding_sample():
    return score_fielding_unit(FieldingUnitInput(
        infield_oaa_score=58,
        outfield_oaa_score=56,
        drs_score=57,
        arm_strength_score=55,
        double_play_score=59,
        range_score=57,
        error_avoidance_score=60,
        positioning_score=58,
    )).model_dump()


@router.get("/baserunner-prevention/sample")
async def baserunner_prevention_sample():
    return score_baserunner_prevention(BaserunnerPreventionInput(
        catcher_throwing_score=56,
        pitcher_hold_score=54,
        infield_tag_score=58,
        outfield_arm_score=57,
        opponent_steal_pressure_score=55,
        opponent_extra_base_pressure_score=56,
    )).model_dump()


@router.get("/defense-v2/sample")
async def defense_v2_sample():
    return calculate_defensive_intelligence(DefensiveIntelligenceInput(
        catcher=CatcherInput(name="Catcher A", framing_score=62, blocking_score=58, throwing_score=56, pop_time_score=55, game_calling_score=60, pitcher_familiarity_score=64, workload_fatigue_score=57),
        fielding=FieldingUnitInput(infield_oaa_score=58, outfield_oaa_score=56, drs_score=57, arm_strength_score=55, double_play_score=59, range_score=57, error_avoidance_score=60, positioning_score=58),
        baserunner_prevention=BaserunnerPreventionInput(catcher_throwing_score=56, pitcher_hold_score=54, infield_tag_score=58, outfield_arm_score=57, opponent_steal_pressure_score=55, opponent_extra_base_pressure_score=56),
        pitcher_contact_profile_score=56,
        park_defensive_difficulty_score=52,
    )).model_dump()
