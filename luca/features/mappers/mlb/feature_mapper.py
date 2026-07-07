from __future__ import annotations

from typing import Any

from luca.intelligence.mlb.adapters import MlbPitcherAdapter
from luca.intelligence.mlb.bsi import BullpenUsageInput, calculate_bsi
from luca.intelligence.mlb.rcp import RunCreationInput, calculate_rcp
from luca.intelligence.mlb.starting_pitcher import calculate_starting_pitcher_score


class MlbFeatureMapper:
    """
    Builds MLB module scores matching SPORT_WEIGHTS["mlb"].
    """

    def __init__(self):
        self.pitcher_adapter = MlbPitcherAdapter()

    def build_modules(
        self,
        game: Any,
        markets: Any | None = None,
        **kwargs: Any,
    ) -> dict[str, float]:
        home_sp_input = self.pitcher_adapter.build_for_home_pitcher(game)
        away_sp_input = self.pitcher_adapter.build_for_away_pitcher(game)

        home_sp = calculate_starting_pitcher_score(home_sp_input)
        away_sp = calculate_starting_pitcher_score(away_sp_input)

        sp_edge = self._edge_score(home_sp.final_sp_score, away_sp.final_sp_score)

        bsi = calculate_bsi(BullpenUsageInput())
        rcp = calculate_rcp(RunCreationInput())
        market_score = self._market_score(markets)

        return {
            "sp": sp_edge,
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

    def _edge_score(self, home_score: float, away_score: float) -> float:
        """
        Converts home-vs-away SP difference into a 0-100 LUCA module score.
        50 = neutral. Above 50 favors home team. Below 50 favors away team.
        """
        return round(max(0.0, min(100.0, 50.0 + (home_score - away_score))), 2)

    def _market_score(self, markets: Any | None) -> float:
        if not markets:
            return 50.0

        return 50.0
