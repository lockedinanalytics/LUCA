from __future__ import annotations

from fastapi import APIRouter

from luca.probability.engine import probability_from_luca_score
from luca.simulation.distributions.score_distribution import ScoreDistributionRequest, simulate_score_distribution

router = APIRouter(prefix="/simulation", tags=["simulation"])


@router.get("/score-distribution")
async def score_distribution(
    game_id: str = "sample",
    home_mean: float = 4.5,
    away_mean: float = 4.2,
    runs: int = 20000,
    spread: float | None = None,
    total: float | None = None,
):
    return simulate_score_distribution(
        ScoreDistributionRequest(game_id=game_id, home_mean=home_mean, away_mean=away_mean, runs=runs),
        spread=spread,
        total=total,
    ).model_dump()


@router.get("/probability")
async def probability(score: float = 55.0, evidence_probability: float | None = None, volatility: float = 0.12):
    return probability_from_luca_score(score, evidence_probability=evidence_probability, volatility=volatility).model_dump()
