from __future__ import annotations

from fastapi import APIRouter

from luca.intelligence.mlb.offense.hitter import score_hitter
from luca.intelligence.mlb.offense.lineup_chain import score_lineup_chain
from luca.intelligence.mlb.offense.models import HitterInput, LineupChainInput, PlatoonInput, RunCreationV2Input
from luca.intelligence.mlb.offense.platoon import score_platoon_fit
from luca.intelligence.mlb.offense.rcp_v2 import calculate_rcp_v2

router = APIRouter(prefix="/intelligence/mlb/offense", tags=["mlb-offense"])


def sample_hitters() -> list[HitterInput]:
    return [
        HitterInput(name="Leadoff A", lineup_spot=1, xwoba_score=62, contact_score=60, chase_discipline_score=58, walk_score=61, baserunning_score=65, platoon_score=55, pitch_type_fit_score=57),
        HitterInput(name="Two B", lineup_spot=2, xwoba_score=59, xslg_score=57, hard_hit_score=56, contact_score=58, walk_score=57, platoon_score=54, pitch_type_fit_score=55),
        HitterInput(name="Three C", lineup_spot=3, xwoba_score=64, xslg_score=66, hard_hit_score=65, barrel_score=64, contact_score=55, platoon_score=58, pitch_type_fit_score=60),
        HitterInput(name="Cleanup D", lineup_spot=4, xwoba_score=61, xslg_score=68, hard_hit_score=67, barrel_score=66, contact_score=52, strikeout_avoidance_score=48, platoon_score=56, pitch_type_fit_score=62),
        HitterInput(name="Five E", lineup_spot=5, xwoba_score=55, xslg_score=57, hard_hit_score=58, barrel_score=56, contact_score=51, platoon_score=53, pitch_type_fit_score=55),
        HitterInput(name="Six F", lineup_spot=6, xwoba_score=52, xslg_score=53, hard_hit_score=52, contact_score=54, platoon_score=50, pitch_type_fit_score=51),
        HitterInput(name="Seven G", lineup_spot=7, xwoba_score=50, xslg_score=51, hard_hit_score=51, contact_score=52, platoon_score=49, pitch_type_fit_score=50),
        HitterInput(name="Eight H", lineup_spot=8, xwoba_score=48, xslg_score=49, hard_hit_score=50, contact_score=50, platoon_score=48, pitch_type_fit_score=49),
        HitterInput(name="Nine I", lineup_spot=9, xwoba_score=47, xslg_score=46, hard_hit_score=48, contact_score=49, platoon_score=47, pitch_type_fit_score=48),
    ]


@router.get("/hitter/sample")
async def hitter_sample():
    return score_hitter(sample_hitters()[2]).model_dump()


@router.get("/lineup-chain/sample")
async def lineup_chain_sample():
    return score_lineup_chain(LineupChainInput(hitters=sample_hitters(), bench_score=54, pinch_hit_score=55)).model_dump()


@router.get("/platoon/sample")
async def platoon_sample():
    return score_platoon_fit(PlatoonInput(
        projected_lhp_plate_appearances=12,
        projected_rhp_plate_appearances=26,
        lineup_platoon_score=56,
        switch_hitter_flex_score=58,
        opposing_bullpen_hand_balance_score=54,
    )).model_dump()


@router.get("/rcp-v2/sample")
async def rcp_v2_sample():
    return calculate_rcp_v2(RunCreationV2Input(
        hitters=sample_hitters(),
        bench_score=54,
        pinch_hit_score=55,
        platoon=PlatoonInput(projected_lhp_plate_appearances=12, projected_rhp_plate_appearances=26, lineup_platoon_score=56, switch_hitter_flex_score=58, opposing_bullpen_hand_balance_score=54),
        park_factor=1.03,
        weather_total_adjustment=0.15,
        opposing_starting_pitcher_score=55,
        opposing_bullpen_score=52,
        expected_plate_appearances=38.8,
    )).model_dump()
