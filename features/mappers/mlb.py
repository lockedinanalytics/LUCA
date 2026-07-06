from __future__ import annotations

from typing import Any

from luca.core.models import MarketLine, TeamGame
from luca.features.mappers.base import FeatureMapper
from luca.intelligence.mlb.bsi import BullpenUsageInput, calculate_bsi
from luca.intelligence.mlb.lineup_quality import LineupQualityInput, calculate_lineup_quality
from luca.intelligence.mlb.rcp import RunCreationInput, calculate_rcp
from luca.intelligence.mlb.starting_pitcher import StartingPitcherInput, calculate_starting_pitcher_score
from luca.intelligence.market.smi import MarketMovementInput, calculate_smi


class MlbFeatureMapper(FeatureMapper):
    def build_modules(self, game: TeamGame, markets: list[MarketLine], context: dict[str, Any] | None = None) -> dict[str, float]:
        context = context or {}

        sp = calculate_starting_pitcher_score(StartingPitcherInput(**context.get("starting_pitcher", {})))
        lineup = calculate_lineup_quality(LineupQualityInput(**context.get("lineup", {})))
        bsi = calculate_bsi(BullpenUsageInput(**context.get("bullpen", {})))
        rcp = calculate_rcp(RunCreationInput(
            top_order_score=lineup.run_creation_score,
            bottom_order_score=lineup.depth_score,
            pitcher_matchup_score=sp.final_sp_score,
            weather_total_adjustment=context.get("weather_total_adjustment", 0.0),
            park_factor=context.get("park_factor", 1.0),
            lineup_count=context.get("lineup", {}).get("lineup_count", 9),
        ))

        first_market = markets[0] if markets else None
        smi = calculate_smi(MarketMovementInput(
            opening_odds=first_market.open_odds if first_market else None,
            current_odds=first_market.current_odds if first_market else None,
            public_percent=context.get("public_percent"),
            sharp_percent=context.get("sharp_percent"),
        ))

        wrm = context.get("wind_run_multiplier", 1.0)

        return {
            "sp": sp.final_sp_score,
            "bsi": bsi.final_bsi,
            "rcp": rcp.rcp_score,
            "smi": smi.smi_score,
            "cam": context.get("cam", 55.0),
            "wrm": max(0, min(100, 50 + (wrm - 1.0) * 100)),
            "umpire": context.get("umpire", 50.0),
            "market_edge": 55.0 if markets else 45.0,
        }
