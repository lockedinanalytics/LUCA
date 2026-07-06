from __future__ import annotations
from typing import List
from luca.core.engine import SportEngine
from luca.core.math_utils import weighted_average
from luca.core.models import LucaRunResult, MarketLine, Sport, TeamGame
from luca.sports.formulas import SPORT_WEIGHTS

class SoccerEngine(SportEngine):
    sport = Sport.SOCCER

    def evaluate_games(self, games: List[TeamGame], markets: List[MarketLine]) -> LucaRunResult:
        return LucaRunResult(
            sport=self.sport,
            league="Soccer",
            date=games[0].date if games else "",
            slate_size=len(games),
            games_evaluated=len(games),
            data_completeness=0.0,
            run_status="formula_ready_stub",
            evaluations=[],
            recommendations=[],
        )

    def score_from_modules(self, modules: dict[str, float]) -> float:
        weights = SPORT_WEIGHTS.get(self.sport.value, {})
        return weighted_average(modules, weights)
