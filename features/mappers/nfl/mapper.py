from __future__ import annotations

from typing import Any

from luca.core.models import MarketLine, TeamGame
from luca.features.mappers.base import FeatureMapper


class NflFeatureMapper(FeatureMapper):
    def build_modules(self, game: TeamGame, markets: list[MarketLine], context: dict[str, Any] | None = None) -> dict[str, float]:
        return {
            "qb_edge": 55.0,
            "ol_dl_edge": 55.0,
            "explosive_play_edge": 55.0,
            "defensive_efficiency_edge": 55.0,
            "injury_edge": 55.0,
            "coaching_edge": 55.0,
            "weather_environment": 50.0,
            "rest_travel": 55.0,
            "market_edge": 55.0 if markets else 45.0,
        }
