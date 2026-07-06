from __future__ import annotations

from collections import defaultdict
from pydantic import BaseModel

from luca.market_tracking.models import MarketSnapshot


class MarketTimeline(BaseModel):
    game_id: str
    market: str
    selection: str
    snapshots: list[MarketSnapshot]
    opening_odds: float | None = None
    current_odds: float | None = None
    closing_odds: float | None = None
    movement: float | None = None


def build_market_timelines(snapshots: list[MarketSnapshot]) -> list[MarketTimeline]:
    grouped = defaultdict(list)
    for snap in snapshots:
        grouped[(snap.game_id, snap.market, snap.selection)].append(snap)

    timelines = []
    for (game_id, market, selection), rows in grouped.items():
        ordered = sorted(rows, key=lambda r: r.timestamp or "")
        opening = ordered[0].odds if ordered else None
        current = ordered[-1].odds if ordered else None
        closing = ordered[-1].odds if ordered and ordered[-1].timestamp == "close" else None
        movement = (current - opening) if current is not None and opening is not None else None
        timelines.append(MarketTimeline(
            game_id=game_id,
            market=market,
            selection=selection,
            snapshots=ordered,
            opening_odds=opening,
            current_odds=current,
            closing_odds=closing,
            movement=round(movement, 3) if movement is not None else None,
        ))
    return timelines
