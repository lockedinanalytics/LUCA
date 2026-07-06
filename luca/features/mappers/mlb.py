from __future__ import annotations

from typing import Any

from luca.core.models import MarketLine, TeamGame
from luca.features.mappers.base import FeatureMapper
from luca.intelligence.mlb.bsi import BullpenUsageInput, calculate_bsi
from luca.intelligence.mlb.bullpen.engine import calculate_bullpen_intelligence
from luca.intelligence.mlb.bullpen.models import BullpenIntelligenceInput
from luca.intelligence.mlb.defense.engine import calculate_defensive_intelligence
from luca.intelligence.mlb.defense.models import DefensiveIntelligenceInput
from luca.intelligence.mlb.environment.engine import calculate_environment_context
from luca.intelligence.mlb.environment.models import EnvironmentContextInput
from luca.intelligence.mlb.lineup_quality import LineupQualityInput, calculate_lineup_quality
from luca.intelligence.mlb.offense.models import RunCreationV2Input
from luca.intelligence.mlb.offense.rcp_v2 import calculate_rcp_v2
from luca.intelligence.mlb.pitching.engine import calculate_starting_pitcher_intelligence
from luca.intelligence.mlb.pitching.models import StartingPitcherIntelligenceInput
from luca.intelligence.mlb.rcp import RunCreationInput, calculate_rcp
from luca.intelligence.market.smi import MarketMovementInput, calculate_smi
from luca.intelligence.market.v2.engine import calculate_smi_v2
from luca.intelligence.market.v2.models import SmartMoneyV2Input


class MlbFeatureMapper(FeatureMapper):
    def build_modules(self, game: TeamGame, markets: list[MarketLine], context: dict[str, Any] | None = None) -> dict[str, float]:
        context = context or {}

        if context.get("environment_context_v2"):
            env = calculate_environment_context(EnvironmentContextInput(**context["environment_context_v2"]))
            wrm_value = env.explainability.get("wind_run_multiplier", 1.0)
            weather_total_adjustment = env.explainability.get("weather_total_adjustment", 0.0)
            umpire_score = env.umpire_score
            environment_score = env.final_environment_score
        else:
            wrm_value = context.get("wind_run_multiplier", 1.0)
            weather_total_adjustment = context.get("weather_total_adjustment", 0.0)
            umpire_score = context.get("umpire", 50.0)
            environment_score = context.get("environment", 50.0)

        if context.get("starting_pitcher_v2"):
            sp = calculate_starting_pitcher_intelligence(StartingPitcherIntelligenceInput(**context["starting_pitcher_v2"]))
            sp_score = sp.final_sp_score
        else:
            sp_score = context.get("sp", 55.0)

        if context.get("bullpen_v2"):
            bsi = calculate_bullpen_intelligence(BullpenIntelligenceInput(**context["bullpen_v2"]))
            bsi_score = bsi.final_bsi
        else:
            bsi_score = calculate_bsi(BullpenUsageInput(**context.get("bullpen", {}))).final_bsi

        if context.get("defense_v2"):
            defense = calculate_defensive_intelligence(DefensiveIntelligenceInput(**context["defense_v2"]))
            cam_score = defense.cam_score
            defense_support = defense.defensive_run_prevention_score
        else:
            cam_score = context.get("cam", 55.0)
            defense_support = context.get("defense_support", 55.0)

        if context.get("offense_v2"):
            offense_payload = dict(context["offense_v2"])
            offense_payload.setdefault("opposing_starting_pitcher_score", sp_score)
            offense_payload.setdefault("opposing_bullpen_score", bsi_score)
            offense_payload.setdefault("weather_total_adjustment", weather_total_adjustment)
            offense_payload.setdefault("park_factor", context.get("park_factor", 1.0))
            rcp_score = calculate_rcp_v2(RunCreationV2Input(**offense_payload)).final_rcp_score
        else:
            lineup = calculate_lineup_quality(LineupQualityInput(**context.get("lineup", {})))
            rcp_score = calculate_rcp(RunCreationInput(
                top_order_score=lineup.run_creation_score,
                bottom_order_score=lineup.depth_score,
                pitcher_matchup_score=sp_score,
                weather_total_adjustment=weather_total_adjustment,
                park_factor=context.get("park_factor", 1.0),
                lineup_count=context.get("lineup", {}).get("lineup_count", 9),
            )).rcp_score

        first_market = markets[0] if markets else None
        if context.get("market_v2"):
            smi_score = calculate_smi_v2(SmartMoneyV2Input(**context["market_v2"])).final_smi_score
        else:
            smi_score = calculate_smi(MarketMovementInput(
                opening_odds=first_market.open_odds if first_market else None,
                current_odds=first_market.current_odds if first_market else None,
                public_percent=context.get("public_percent"),
                sharp_percent=context.get("sharp_percent"),
            )).smi_score

        return {
            "sp": sp_score,
            "bsi": bsi_score,
            "rcp": rcp_score,
            "smi": smi_score,
            "cam": cam_score,
            "wrm": max(0, min(100, 50 + (wrm_value - 1.0) * 100)),
            "umpire": umpire_score,
            "market_edge": 55.0 if markets else 45.0,
            "defense_support": defense_support,
            "environment": environment_score,
        }
