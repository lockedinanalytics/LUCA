from __future__ import annotations

from typing import Any

from luca.core.models import MarketLine, TeamGame
from luca.features.mappers.base import FeatureMapper


class SoccerFeatureMapper(FeatureMapper):
    def build_modules(self, game: TeamGame, markets: list[MarketLine], context: dict[str, Any] | None = None) -> dict[str, float]:
        return {
            "xg_edge": 55.0,
            "defensive_xga_edge": 55.0,
            "tactical_matchup": 55.0,
            "squad_availability": 55.0,
            "goalkeeper_edge": 55.0,
            "fixture_congestion": 50.0,
            "set_piece_edge": 55.0,
            "referee_edge": 50.0,
            "market_edge": 55.0 if markets else 45.0,
        }
