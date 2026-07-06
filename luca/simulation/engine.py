from __future__ import annotations

import math
import random
from collections import Counter

from luca.simulation.models import SimulationRequest, SimulationResult


def _poisson_sample(lam: float) -> int:
    lam = max(0.05, float(lam))
    limit = math.exp(-lam)
    k = 0
    p = 1.0
    while p > limit:
        k += 1
        p *= random.random()
    return k - 1


def simulate_game(request: SimulationRequest, seed: int | None = 42) -> SimulationResult:
    if seed is not None:
        random.seed(seed)

    home_wins = 0
    away_wins = 0
    home_scores: list[int] = []
    away_scores: list[int] = []
    outcomes: Counter[str] = Counter()

    for _ in range(request.runs):
        home = _poisson_sample(request.mean_home)
        away = _poisson_sample(request.mean_away)

        if home == away:
            if random.random() >= 0.5:
                home += 1
            else:
                away += 1

        home_scores.append(home)
        away_scores.append(away)
        outcomes[f"{away}-{home}"] += 1

        if home > away:
            home_wins += 1
        else:
            away_wins += 1

    mean_home = sum(home_scores) / request.runs
    mean_away = sum(away_scores) / request.runs
    totals = [h + a for h, a in zip(home_scores, away_scores)]
    mean_total = sum(totals) / request.runs
    variance = sum((x - mean_total) ** 2 for x in totals) / request.runs

    distribution = {score: count / request.runs for score, count in outcomes.most_common(20)}
    entropy = -sum(p * math.log(p) for p in distribution.values() if p > 0)

    return SimulationResult(
        game_id=request.game_id,
        runs=request.runs,
        home_win_probability=home_wins / request.runs,
        away_win_probability=away_wins / request.runs,
        projected_home_score=round(mean_home, 3),
        projected_away_score=round(mean_away, 3),
        projected_total=round(mean_total, 3),
        projected_margin=round(mean_home - mean_away, 3),
        variance=round(variance, 3),
        entropy=round(entropy, 3),
        distribution=distribution,
    )
