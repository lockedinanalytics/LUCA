from __future__ import annotations

from typing import Any

from luca.intelligence.mlb.bsi import BullpenUsageInput, calculate_bsi
from luca.intelligence.mlb.rcp import RunCreationInput, calculate_rcp
from luca.intelligence.mlb.starting_pitcher import (
    StartingPitcherInput,
    calculate_starting_pitcher_score,
)


class MlbFeatureMapper:
    """
    Builds MLB module scores matching SPORT_WEIGHTS["mlb"].
    """

    def build_modules(
        self,
        game: Any,
        markets: Any | None = None,
        **kwargs: Any,
    ) -> dict[str, float]:
        sp = calculate_starting_pitcher_score(StartingPitcherInput())
        bsi = calculate_bsi(BullpenUsageInput())
        rcp = calculate_rcp(RunCreationInput())

        market_score = self._market_score(markets)

        return {
            "sp": sp.final_sp_score,
            "bsi": bsi.final_bsi,
            "rcp": rcp.rcp_score,
            "smi": market_score,
            "cam": 50.0,
            "wrm": 50.0,
            "umpire": 50.0,
            "market_edge": market_score,
        }

    def build_many(self, games: list[Any]) -> list[dict[str, float]]:
        return [self.build_modules(game) for game in games]

    def _market_score(self, markets: Any | None) -> float:
        if not markets:
            return 50.0

        return 50.0
