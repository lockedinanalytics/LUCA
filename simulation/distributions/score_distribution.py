from __future__ import annotations

import math
import random
from collections import Counter
from pydantic import BaseModel


class ScoreDistributionRequest(BaseModel):
    game_id: str
    home_mean: float
    away_mean: float
    runs: int = 20000
    allow_ties: bool = False


class ScoreDistributionResult(BaseModel):
    game_id: str
    runs: int
    home_win_probability: float
    away_win_probability: float
    draw_probability: float
    cover_probability: float | None = None
    over_probability: float | None = None
    projected_home_score: float
    projected_away_score: float
    projected_total: float
    projected_margin: float
    variance: float
    p10_total: float
    p50_total: float
    p90_total: float
    top_scores: dict[str, float]


def _poisson(lam: float) -> int:
    lam = max(0.05, float(lam))
    limit = math.exp(-lam)
    k = 0
    p = 1.0
    while p > limit:
        k += 1
        p *= random.random()
    return k - 1


def _percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    idx = min(len(ordered) - 1, max(0, int(round((pct / 100) * (len(ordered) - 1)))))
    return float(ordered[idx])


def simulate_score_distribution(
    request: ScoreDistributionRequest,
    spread: float | None = None,
    total: float | None = None,
    seed: int | None = 42,
) -> ScoreDistributionResult:
    if seed is not None:
        random.seed(seed)

    home_scores: list[int] = []
    away_scores: list[int] = []
    totals: list[int] = []
    top: Counter[str] = Counter()
    home_wins = away_wins = draws = covers = overs = 0

    for _ in range(request.runs):
        home = _poisson(request.home_mean)
        away = _poisson(request.away_mean)

        if not request.allow_ties and home == away:
            if random.random() >= 0.5:
                home += 1
            else:
                away += 1

        home_scores.append(home)
        away_scores.append(away)
        totals.append(home + away)
        top[f"{away}-{home}"] += 1

        if home > away:
            home_wins += 1
        elif away > home:
            away_wins += 1
        else:
            draws += 1

        if spread is not None and (home + spread) > away:
            covers += 1
        if total is not None and (home + away) > total:
            overs += 1

    mean_home = sum(home_scores) / request.runs
    mean_away = sum(away_scores) / request.runs
    mean_total = sum(totals) / request.runs
    variance = sum((x - mean_total) ** 2 for x in totals) / request.runs

    return ScoreDistributionResult(
        game_id=request.game_id,
        runs=request.runs,
        home_win_probability=round(home_wins / request.runs, 5),
        away_win_probability=round(away_wins / request.runs, 5),
        draw_probability=round(draws / request.runs, 5),
        cover_probability=round(covers / request.runs, 5) if spread is not None else None,
        over_probability=round(overs / request.runs, 5) if total is not None else None,
        projected_home_score=round(mean_home, 3),
        projected_away_score=round(mean_away, 3),
        projected_total=round(mean_total, 3),
        projected_margin=round(mean_home - mean_away, 3),
        variance=round(variance, 3),
        p10_total=round(_percentile(totals, 10), 3),
        p50_total=round(_percentile(totals, 50), 3),
        p90_total=round(_percentile(totals, 90), 3),
        top_scores={score: round(count / request.runs, 5) for score, count in top.most_common(10)},
    )
