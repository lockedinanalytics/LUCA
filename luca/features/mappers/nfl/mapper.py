from __future__ import annotations

from typing import Any

from luca.core.models import MarketLine, TeamGame
from luca.features.mappers.base import FeatureMapper
from luca.intelligence.nfl.quarterback.engine import calculate_nfl_quarterback_intelligence
from luca.intelligence.nfl.quarterback.models import NflQuarterbackIntelligenceInput


class NflFeatureMapper(FeatureMapper):
    def build_modules(self, game: TeamGame, markets: list[MarketLine], context: dict[str, Any] | None = None) -> dict[str, float]:
        context = context or {}

        if context.get("quarterback_v2"):
            qb = calculate_nfl_quarterback_intelligence(NflQuarterbackIntelligenceInput(**context["quarterback_v2"]))
            qb_score = qb.final_qb_score
            explosive_score = qb.explosive_passing_score
            variance_penalty = qb.volatility_score
        else:
            qb_score = context.get("qb_edge", 55.0)
            explosive_score = context.get("explosive_play_edge", 55.0)
            variance_penalty = 50.0

        return {
            "qb_edge": qb_score,
            "ol_dl_edge": context.get("ol_dl_edge", 55.0),
            "explosive_play_edge": explosive_score,
            "defensive_efficiency_edge": context.get("defensive_efficiency_edge", 55.0),
            "injury_edge": context.get("injury_edge", 55.0),
            "coaching_edge": context.get("coaching_edge", 55.0),
            "weather_environment": context.get("weather_environment", 50.0),
            "rest_travel": context.get("rest_travel", 55.0),
            "market_edge": 55.0 if markets else 45.0,
            "qb_volatility": variance_penalty,
        }
