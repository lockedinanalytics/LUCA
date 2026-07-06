from __future__ import annotations

from fastapi import APIRouter

from luca.intelligence.mlb.lineup_quality import LineupQualityInput, calculate_lineup_quality
from luca.intelligence.mlb.starting_pitcher import StartingPitcherInput, calculate_starting_pitcher_score

router = APIRouter(prefix="/intelligence/mlb", tags=["mlb-intelligence"])


@router.get("/starting-pitcher/sample")
async def starting_pitcher_sample(
    xera: float = 3.75,
    fip: float = 3.9,
    strikeout_rate: float = 25,
    walk_rate: float = 7.5,
    hard_hit_rate: float = 38,
    barrel_rate: float = 7,
    recent_pitch_count: int = 92,
    days_rest: int = 5,
):
    return calculate_starting_pitcher_score(StartingPitcherInput(
        xera=xera,
        fip=fip,
        strikeout_rate=strikeout_rate,
        walk_rate=walk_rate,
        hard_hit_rate=hard_hit_rate,
        barrel_rate=barrel_rate,
        recent_pitch_count=recent_pitch_count,
        days_rest=days_rest,
    )).model_dump()


@router.get("/lineup-quality/sample")
async def lineup_quality_sample(
    top_four_xwoba_score: float = 58,
    bottom_five_xwoba_score: float = 52,
    platoon_advantage_score: float = 55,
    strikeout_risk_score: float = 54,
    power_score: float = 57,
):
    return calculate_lineup_quality(LineupQualityInput(
        top_four_xwoba_score=top_four_xwoba_score,
        bottom_five_xwoba_score=bottom_five_xwoba_score,
        platoon_advantage_score=platoon_advantage_score,
        strikeout_risk_score=strikeout_risk_score,
        power_score=power_score,
    )).model_dump()
