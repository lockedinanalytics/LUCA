from __future__ import annotations

from fastapi import APIRouter

from luca.intelligence.nfl.trench.defensive_front import score_defensive_front
from luca.intelligence.nfl.trench.matchup import calculate_trench_matchup
from luca.intelligence.nfl.trench.models import DefensiveFrontInput, OffensiveLineInput, TrenchMatchupInput
from luca.intelligence.nfl.trench.offensive_line import score_offensive_line

router = APIRouter(prefix="/intelligence/nfl/trench", tags=["nfl-trench"])


@router.get("/offensive-line/sample")
async def offensive_line_sample():
    return score_offensive_line(OffensiveLineInput(
        pass_block_win_rate=64,
        run_block_win_rate=72,
        pressure_allowed_rate=29,
        sack_responsibility_rate=5.8,
        blitz_pickup_score=61,
        interior_protection_score=58,
        edge_protection_score=60,
        short_yardage_score=59,
        goal_line_blocking_score=58,
        continuity_score=63,
        depth_quality_score=57,
    )).model_dump()


@router.get("/defensive-front/sample")
async def defensive_front_sample():
    return score_defensive_front(DefensiveFrontInput(
        pressure_rate=37,
        quick_pressure_rate=13.5,
        sack_conversion_rate=18.5,
        pass_rush_win_rate=44,
        run_stop_win_rate=33,
        stuff_rate=20,
        missed_tackle_rate=9.5,
        gap_integrity_score=57,
        edge_containment_score=56,
        interior_disruption_score=60,
        rotation_depth_score=58,
    )).model_dump()


@router.get("/matchup/sample")
async def matchup_sample():
    return calculate_trench_matchup(TrenchMatchupInput(
        offensive_line=OffensiveLineInput(pass_block_win_rate=64, run_block_win_rate=72, pressure_allowed_rate=29, sack_responsibility_rate=5.8, blitz_pickup_score=61, interior_protection_score=58, edge_protection_score=60, short_yardage_score=59, goal_line_blocking_score=58, continuity_score=63, depth_quality_score=57),
        defensive_front=DefensiveFrontInput(pressure_rate=37, quick_pressure_rate=13.5, sack_conversion_rate=18.5, pass_rush_win_rate=44, run_stop_win_rate=33, stuff_rate=20, missed_tackle_rate=9.5, gap_integrity_score=57, edge_containment_score=56, interior_disruption_score=60, rotation_depth_score=58),
        quarterback_pressure_resilience_score=61,
        running_back_vision_score=58,
        offensive_scheme_score=59,
        defensive_scheme_score=55,
        weather_surface_score=52,
    )).model_dump()
