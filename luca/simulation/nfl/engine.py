from __future__ import annotations

import random
from collections import Counter

from luca.simulation.nfl.models import NflSimulationInput, NflSimulationOutput


def _normal(mu: float, sigma: float) -> float:
    return random.gauss(mu, sigma)


def _percentile(values: list[float], pct: float) -> float:
    ordered = sorted(values)
    if not ordered:
        return 0.0
    idx = min(len(ordered) - 1, max(0, int(round((pct / 100) * (len(ordered) - 1)))))
    return ordered[idx]


def simulate_nfl_game(row: NflSimulationInput, spread: float | None = None, total: float | None = None, seed: int | None = 42) -> NflSimulationOutput:
    if seed is not None:
        random.seed(seed)

    home_mean = row.total_baseline / 2
    away_mean = row.total_baseline / 2

    home_mean += (row.home_offense_score - row.away_defense_score) * 0.08
    away_mean += (row.away_offense_score - row.home_defense_score) * 0.08
    home_mean += (row.home_context_score - 50) * 0.035
    away_mean += (row.away_context_score - 50) * 0.030
    home_mean += (row.home_market_score - 50) * 0.020
    away_mean += (row.away_market_score - 50) * 0.020
    home_mean += row.home_field_edge

    home_scores = []
    away_scores = []
    totals = []
    margins = []
    bands = Counter()
    home_wins = away_wins = covers = overs = 0

    variance_base = 7.5 + abs(row.home_offense_score - row.away_offense_score) * 0.025

    for _ in range(row.runs):
        home = max(0, round(_normal(home_mean, variance_base)))
        away = max(0, round(_normal(away_mean, variance_base)))

        if home == away:
            if random.random() >= 0.5:
                home += 3
            else:
                away += 3

        home_scores.append(home)
        away_scores.append(away)
        totals.append(home + away)
        margins.append(home - away)

        if home > away:
            home_wins += 1
        else:
            away_wins += 1

        if spread is not None and home + spread > away:
            covers += 1
        if total is not None and home + away > total:
            overs += 1

        total_band = int((home + away) // 7 * 7)
        bands[f"{total_band}-{total_band + 6}"] += 1

    mean_home = sum(home_scores) / row.runs
    mean_away = sum(away_scores) / row.runs
    mean_total = sum(totals) / row.runs
    mean_margin = sum(margins) / row.runs

    total_var = sum((x - mean_total) ** 2 for x in totals) / row.runs
    margin_var = sum((x - mean_margin) ** 2 for x in margins) / row.runs

    return NflSimulationOutput(
        game_id=row.game_id,
        home_win_probability=round(home_wins / row.runs, 5),
        away_win_probability=round(away_wins / row.runs, 5),
        projected_home_score=round(mean_home, 3),
        projected_away_score=round(mean_away, 3),
        projected_total=round(mean_total, 3),
        projected_margin=round(mean_margin, 3),
        spread_cover_probability=round(covers / row.runs, 5) if spread is not None else None,
        over_probability=round(overs / row.runs, 5) if total is not None else None,
        total_variance=round(total_var, 3),
        margin_variance=round(margin_var, 3),
        confidence_interval_total=(round(_percentile(totals, 10), 3), round(_percentile(totals, 90), 3)),
        confidence_interval_margin=(round(_percentile(margins, 10), 3), round(_percentile(margins, 90), 3)),
        top_score_bands={k: round(v / row.runs, 5) for k, v in bands.most_common(8)},
    )
