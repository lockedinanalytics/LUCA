from __future__ import annotations

from typing import Any

from luca.core.models import MarketLine, TeamGame
from luca.features.mappers.base import FeatureMapper


class NcaafFeatureMapper(FeatureMapper):
    def build_modules(self, game: TeamGame, markets: list[MarketLine], context: dict[str, Any] | None = None) -> dict[str, float]:
        return {
            "team_power_edge": 55.0,
            "qb_development_edge": 55.0,
            "explosive_play_edge": 55.0,
            "talent_composite_edge": 55.0,
            "coaching_edge": 55.0,
            "motivation_spot_edge": 50.0,
            "home_field_edge": 55.0,
            "defensive_havoc_edge": 55.0,
            "market_edge": 55.0 if markets else 45.0,
        }
