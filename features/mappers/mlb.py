from __future__ import annotations

from typing import Any

from luca.core.models import MarketLine, TeamGame
from luca.features.mappers.base import FeatureMapper
from luca.intelligence.mlb.bsi import BullpenUsageInput, calculate_bsi
from luca.intelligence.mlb.rcp import RunCreationInput, calculate_rcp
from luca.intelligence.market.smi import MarketMovementInput, calculate_smi


class MlbFeatureMapper(FeatureMapper):
    def build_modules(self, game: TeamGame, markets: list[MarketLine], context: dict[str, Any] | None = None) -> dict[str, float]:
        context = context or {}

        bsi = calculate_bsi(BullpenUsageInput(**context.get("bullpen", {})))
        rcp = calculate_rcp(RunCreationInput(**context.get("run_creation", {})))

        first_market = markets[0] if markets else None
        smi = calculate_smi(MarketMovementInput(
            opening_odds=first_market.open_odds if first_market else None,
            current_odds=first_market.current_odds if first_market else None,
            public_percent=context.get("public_percent"),
            sharp_percent=context.get("sharp_percent"),
        ))

        weather_score = context.get("weather_score", 50.0)
        wrm = context.get("wind_run_multiplier", 1.0)

        return {
            "sp": context.get("sp", 55.0),
            "bsi": bsi.final_bsi,
            "rcp": rcp.rcp_score,
            "smi": smi.smi_score,
            "cam": context.get("cam", 55.0),
            "wrm": max(0, min(100, 50 + (wrm - 1.0) * 100)),
            "umpire": context.get("umpire", 50.0),
            "market_edge": 55.0 if markets else 45.0,
        }
