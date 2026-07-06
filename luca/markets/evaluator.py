from __future__ import annotations

from luca.core.models import MarketLine, MarketType
from luca.markets.models import MarketEvaluation
from luca.objectives.engines import moneyline_edge, spread_edge, totals_edge


def evaluate_market(
    line: MarketLine,
    projected_probability: float | None = None,
    projected_margin: float | None = None,
    projected_total: float | None = None,
) -> MarketEvaluation:
    if line.market_type == MarketType.MONEYLINE:
        if projected_probability is None:
            raise ValueError("projected_probability required for moneyline")
        data = moneyline_edge(projected_probability, line.current_odds or -110)
        return MarketEvaluation(
            market=line.market_type.value,
            selection=line.selection,
            projected_probability=data["projected_probability"],
            implied_probability=data["market_implied_probability"],
            edge=data["edge"],
            tier=data["tier"],
        )

    if line.market_type == MarketType.SPREAD:
        if projected_margin is None or line.spread is None:
            raise ValueError("projected_margin and spread required")
        data = spread_edge(projected_margin, line.spread)
        return MarketEvaluation(
            market=line.market_type.value,
            selection=line.selection,
            projected_value=data["projected_margin"],
            market_value=data["market_spread"],
            edge=data["spread_edge_points"],
            tier=data["tier"],
        )

    if line.market_type == MarketType.TOTAL:
        if projected_total is None or line.total is None:
            raise ValueError("projected_total and total required")
        data = totals_edge(projected_total, line.total)
        return MarketEvaluation(
            market=line.market_type.value,
            selection=data["side"],
            projected_value=data["projected_total"],
            market_value=data["market_total"],
            edge=data["edge_points"],
            tier=data["tier"],
        )

    return MarketEvaluation(
        market=line.market_type.value,
        selection=line.selection,
        edge=0.0,
        tier="pass",
        notes=["Unsupported market type in v7 evaluator."],
    )
