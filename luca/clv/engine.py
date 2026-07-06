from __future__ import annotations

from pydantic import BaseModel


class ClvResult(BaseModel):
    published_odds: float | None
    closing_odds: float | None
    clv_points: float | None
    beat_close: bool | None
    notes: list[str]


def calculate_clv(published_odds: float | None, closing_odds: float | None) -> ClvResult:
    if published_odds is None or closing_odds is None:
        return ClvResult(published_odds=published_odds, closing_odds=closing_odds, clv_points=None, beat_close=None, notes=["Missing odds for CLV."])

    # For American odds, more favorable depends on side. This initial version treats lower negative / higher positive as better for the bettor.
    clv = closing_odds - published_odds
    beat = published_odds > closing_odds if published_odds < 0 and closing_odds < 0 else published_odds < closing_odds

    return ClvResult(
        published_odds=published_odds,
        closing_odds=closing_odds,
        clv_points=round(clv, 3),
        beat_close=beat,
        notes=["Phase 6 CLV shell; phase 7 should normalize by implied probability."],
    )
