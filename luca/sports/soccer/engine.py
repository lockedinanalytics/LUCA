from __future__ import annotations

from typing import List

from luca.core.engine import SportEngine
from luca.core.models import LucaRunResult, MarketLine, Sport, TeamGame


class SoccerEngine(SportEngine):
    sport = Sport.SOCCER

    def evaluate_games(self, games: List[TeamGame], markets: List[MarketLine]) -> LucaRunResult:
        # Placeholder production contract.
        # Next pass will add sport-specific scoring formulas and provider mappings.
        return LucaRunResult(
            sport=self.sport,
            league="Soccer",
            date=games[0].date if games else "",
            slate_size=len(games),
            games_evaluated=len(games),
            data_completeness=0.0,
            run_status="stub",
            evaluations=[],
            recommendations=[],
        )
