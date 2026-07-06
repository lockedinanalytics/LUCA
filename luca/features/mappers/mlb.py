from __future__ import annotations

from typing import Any

from luca.core.models import MarketLine, TeamGame
from luca.features.mappers.base import FeatureMapper


class MlbFeatureMapper(FeatureMapper):
    def build_modules(self, game: TeamGame, markets: list[MarketLine], context: dict[str, Any] | None = None) -> dict[str, float]:
        # Phase 2 creates the mapper contract. Phase 3 fills these with real Statcast/lineup/bullpen features.
        return {
            "sp": 55.0,
            "bsi": 55.0,
            "rcp": 55.0,
            "smi": 55.0 if markets else 45.0,
            "cam": 55.0,
            "wrm": 50.0,
            "umpire": 50.0,
            "market_edge": 55.0 if markets else 45.0,
        }
