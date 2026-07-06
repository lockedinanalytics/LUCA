from __future__ import annotations

from luca.core.math_utils import american_to_implied_probability


def clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, float(value)))


def odds_delta_to_score(delta: float | None) -> float:
    if delta is None:
        return 50.0
    return clamp(50 + abs(delta) * 0.35)


def implied_probability_delta(opening_odds: float | None, current_odds: float | None) -> float | None:
    if opening_odds is None or current_odds is None:
        return None
    return american_to_implied_probability(current_odds) - american_to_implied_probability(opening_odds)
