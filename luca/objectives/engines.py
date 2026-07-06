from __future__ import annotations
from luca.core.math_utils import american_to_implied_probability

def edge_tier(edge: float) -> str:
    if edge >= .06: return "strong"
    if edge >= .04: return "playable"
    if edge >= .02: return "lean"
    return "pass"

def moneyline_edge(projected_probability: float, american_odds: float) -> dict:
    implied = american_to_implied_probability(american_odds)
    edge = projected_probability - implied
    return {"projected_probability": projected_probability, "market_implied_probability": implied, "edge": edge, "positive_ev": edge > 0, "tier": edge_tier(edge)}

def spread_edge(projected_margin: float, market_spread: float) -> dict:
    edge = projected_margin - market_spread
    ae = abs(edge)
    tier = "strong" if ae >= 3.1 else "playable" if ae >= 2.1 else "lean" if ae >= 1.1 else "pass"
    return {"projected_margin": projected_margin, "market_spread": market_spread, "spread_edge_points": edge, "tier": tier}

def totals_edge(projected_total: float, market_total: float) -> dict:
    edge = projected_total - market_total
    ae = abs(edge)
    tier = "strong" if ae >= 2 else "playable" if ae >= 1 else "lean" if ae >= .5 else "pass"
    return {"projected_total": projected_total, "market_total": market_total, "edge_points": edge, "side": "over" if edge > 0 else "under", "tier": tier}
