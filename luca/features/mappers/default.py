from __future__ import annotations

from typing import Any

from luca.core.models import MarketLine, TeamGame
from luca.features.mappers.base import FeatureMapper
from luca.sports.formulas import SPORT_WEIGHTS


class DefaultFeatureMapper(FeatureMapper):
    def build_modules(self, game: TeamGame, markets: list[MarketLine], context: dict[str, Any] | None = None) -> dict[str, float]:
        weights = SPORT_WEIGHTS.get(game.sport.value, {})
        modules = {key: 55.0 for key in weights} if weights else {"generic_power": 55.0}
        if not markets:
            modules["market_edge"] = min(modules.get("market_edge", 50.0), 45.0)
        return modules
