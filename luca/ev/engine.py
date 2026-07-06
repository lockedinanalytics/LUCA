from __future__ import annotations

from pydantic import BaseModel

from luca.core.math_utils import american_to_implied_probability


class ExpectedValueResult(BaseModel):
    projected_probability: float
    implied_probability: float
    edge: float
    fair_odds: float
    expected_value_per_unit: float
    risk_adjusted_ev: float
    tier: str


def probability_to_fair_american(probability: float) -> float:
    p = min(max(probability, 0.001), 0.999)
    if p >= 0.5:
        return round(-100 * p / (1 - p), 2)
    return round(100 * (1 - p) / p, 2)


def calculate_ev(projected_probability: float, american_odds: float, risk_penalty: float = 0.0) -> ExpectedValueResult:
    implied = american_to_implied_probability(american_odds)
    edge = projected_probability - implied

    if american_odds < 0:
        profit_per_unit = 100 / abs(american_odds)
    else:
        profit_per_unit = american_odds / 100

    ev = projected_probability * profit_per_unit - (1 - projected_probability)
    risk_adjusted = ev - abs(risk_penalty)

    if risk_adjusted >= 0.08:
        tier = "strong"
    elif risk_adjusted >= 0.04:
        tier = "playable"
    elif risk_adjusted > 0:
        tier = "lean"
    else:
        tier = "pass"

    return ExpectedValueResult(
        projected_probability=round(projected_probability, 5),
        implied_probability=round(implied, 5),
        edge=round(edge, 5),
        fair_odds=probability_to_fair_american(projected_probability),
        expected_value_per_unit=round(ev, 5),
        risk_adjusted_ev=round(risk_adjusted, 5),
        tier=tier,
    )
