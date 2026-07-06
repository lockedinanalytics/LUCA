from __future__ import annotations

from fastapi import APIRouter

from luca.core.models import MarketType, Sport
from luca.decision.engine import DecisionInput, make_decision
from luca.ev.engine import calculate_ev
from luca.risk.engine import RiskInput, calculate_risk

router = APIRouter(prefix="/decision", tags=["decision"])


@router.get("/ev")
async def ev(projected_probability: float = 0.56, odds: float = -110, risk_penalty: float = 0.015):
    return calculate_ev(projected_probability, odds, risk_penalty).model_dump()


@router.get("/risk")
async def risk(variance: float = 1.0, data_completeness: float = 0.80, volatility: float = 0.12):
    return calculate_risk(RiskInput(variance=variance, data_completeness=data_completeness, volatility=volatility)).model_dump()


@router.get("/sample")
async def sample_decision(
    sport: Sport = Sport.MLB,
    league: str = "MLB",
    game_id: str = "sample",
    selection: str = "Home Sample",
    odds: float = -110,
    luca_score: float = 58,
    projected_probability: float = 0.56,
    confidence: float = 78,
):
    return make_decision(DecisionInput(
        sport=sport,
        league=league,
        game_id=game_id,
        market_type=MarketType.MONEYLINE,
        selection=selection,
        odds=odds,
        luca_score=luca_score,
        projected_probability=projected_probability,
        confidence=confidence,
    )).model_dump()
