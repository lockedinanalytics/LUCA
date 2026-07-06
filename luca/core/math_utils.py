from __future__ import annotations

from math import exp


def clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, float(value)))


def weighted_average(values: dict[str, float], weights: dict[str, float], default: float = 50.0) -> float:
    total_weight = sum(weights.values())
    if total_weight <= 0:
        return default
    score = 0.0
    for key, weight in weights.items():
        score += float(values.get(key, default)) * weight
    return score / total_weight


def american_to_implied_probability(odds: float) -> float:
    odds = float(odds)
    if odds < 0:
        return abs(odds) / (abs(odds) + 100.0)
    return 100.0 / (odds + 100.0)


def probability_to_american(probability: float) -> float:
    p = min(max(float(probability), 0.0001), 0.9999)
    if p >= 0.5:
        return -100.0 * p / (1.0 - p)
    return 100.0 * (1.0 - p) / p


def logistic(x: float) -> float:
    return 1.0 / (1.0 + exp(-float(x)))


def edge_probability(projected_probability: float, market_implied_probability: float) -> float:
    return float(projected_probability) - float(market_implied_probability)
