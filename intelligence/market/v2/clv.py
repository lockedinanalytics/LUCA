from __future__ import annotations

from luca.core.math_utils import american_to_implied_probability
from luca.intelligence.market.v2.models import ClvInput, ClvOutput
from luca.intelligence.market.v2.utils import clamp


def score_clv(row: ClvInput) -> ClvOutput:
    warnings: list[str] = []

    if row.published_odds is None or row.closing_odds is None:
        return ClvOutput(
            clv_implied_probability_delta=None,
            beat_close=None,
            clv_score=50.0,
            warnings=["Published or closing odds missing."],
        )

    published_implied = american_to_implied_probability(row.published_odds)
    closing_implied = american_to_implied_probability(row.closing_odds)
    delta = closing_implied - published_implied

    # If the market closed more expensive than published, the pick beat the close.
    beat_close = delta > 0
    score = 50 + delta * 900

    if beat_close and delta >= 0.02:
        warnings.append("Strong positive CLV signal.")
    elif not beat_close and delta <= -0.02:
        warnings.append("Negative CLV signal.")

    if row.projected_probability is not None:
        model_to_close = row.projected_probability - closing_implied
        score += model_to_close * 120

    return ClvOutput(
        clv_implied_probability_delta=round(delta, 5),
        beat_close=beat_close,
        clv_score=round(clamp(score), 2),
        warnings=warnings,
    )
