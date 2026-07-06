from __future__ import annotations

from fastapi import APIRouter

from luca.decision.nfl.engine import make_nfl_unified_decision
from luca.decision.nfl.models import NflUnifiedDecisionInput
from luca.simulation.nfl.engine import simulate_nfl_game
from luca.simulation.nfl.models import NflSimulationInput

router = APIRouter(prefix="/decision/nfl", tags=["nfl-decision"])


@router.get("/simulation/sample")
async def nfl_simulation_sample():
    return simulate_nfl_game(NflSimulationInput(
        game_id="sample",
        home_team="Home",
        away_team="Away",
        home_offense_score=58,
        away_offense_score=51,
        home_defense_score=55,
        away_defense_score=50,
        home_context_score=56,
        home_market_score=57,
        total_baseline=45.5,
        home_field_edge=1.8,
        runs=12000,
    ), spread=-3.0, total=45.5).model_dump()


@router.get("/unified/sample")
async def nfl_unified_sample():
    return make_nfl_unified_decision(NflUnifiedDecisionInput(
        game_id="sample",
        home_team="Home",
        away_team="Away",
        market_type="spread",
        selection="Home",
        odds=-110,
        spread=-3.0,
        total=45.5,
        quarterback_score=62,
        trench_score=58,
        skill_coverage_score=59,
        context_score=56,
        market_score=57,
        defense_score=55,
        injury_score=54,
    )).model_dump()
