from __future__ import annotations

from luca.intelligence.market.v2.models import MarketContradictionInput, MarketContradictionOutput
from luca.intelligence.market.v2.utils import clamp


def score_market_contradiction(row: MarketContradictionInput) -> MarketContradictionOutput:
    warnings: list[str] = []

    agreement = 100 - abs(row.model_edge_score - row.market_support_score)
    contradiction = abs(row.model_edge_score - row.market_support_score)

    if row.reverse_line_movement:
        contradiction += 12
        warnings.append("Reverse line movement detected.")

    if row.public_percent is not None and row.sharp_percent is not None:
        diff = row.sharp_percent - row.public_percent
        if row.model_edge_score >= 58 and diff <= -15:
            contradiction += 10
            warnings.append("Model likes side but sharp/public signal disagrees.")
        elif row.model_edge_score <= 45 and diff >= 15:
            contradiction += 8
            warnings.append("Market supports side while model is weak.")

    return MarketContradictionOutput(
        contradiction_score=round(clamp(contradiction), 2),
        agreement_score=round(clamp(agreement), 2),
        warnings=warnings,
    )
