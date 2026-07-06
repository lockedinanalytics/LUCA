from __future__ import annotations

from luca.core.math_utils import american_to_implied_probability, edge_probability


def moneyline_edge(projected_probability: float, american_odds: float) -> dict:
    implied = american_to_implied_probability(american_odds)
    edge = edge_probability(projected_probability, implied)
    return {
        "projected_probability": projected_probability,
        "market_implied_probability": implied,
        "edge": edge,
        "positive_ev": edge > 0,
    }


def spread_edge(projected_margin: float, market_spread: float) -> dict:
    edge = projected_margin - market_spread
    return {
        "projected_margin": projected_margin,
        "market_spread": market_spread,
        "spread_edge_points": edge,
        "positive_edge": abs(edge) >= 1.5,
    }


def totals_edge(projected_total: float, market_total: float) -> dict:
    edge = projected_total - market_total
    side = "over" if edge > 0 else "under"
    return {
        "projected_total": projected_total,
        "market_total": market_total,
        "edge_points": edge,
        "side": side,
        "positive_edge": abs(edge) >= 0.5,
    }
