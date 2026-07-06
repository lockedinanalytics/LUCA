from __future__ import annotations

from typing import List

from luca.analytics.engines import confidence_integrity, decision_quality, luca_composite_intelligence
from luca.core.engine import SportEngine
from luca.core.math_utils import logistic, weighted_average
from luca.core.models import GameEvaluation, LucaRunResult, MarketLine, MarketType, ModuleScores, PickRecommendation, Sport, TeamGame
from luca.features.mappers.factory import get_feature_mapper
from luca.governance.engine import apply_governance, assign_category
from luca.objectives.engines import moneyline_edge
from luca.sports.formulas import SPORT_WEIGHTS
from luca.units.engine import assign_units

class SoccerEngine(SportEngine):
    sport = Sport.SOCCER

    def evaluate_games(self, games: List[TeamGame], markets: List[MarketLine]) -> LucaRunResult:
        evaluations, recommendations, pass_list = [], [], []
        mapper = get_feature_mapper(self.sport)

        for game in games:
            game_markets = [m for m in markets if m.game_id == game.game_id]
            modules = mapper.build_modules(game=game, markets=game_markets)
            score = weighted_average(modules, SPORT_WEIGHTS.get(self.sport.value, {}))
            probability = logistic((score - 50.0) / 12.0)

            line = next((m for m in game_markets if m.market_type == MarketType.MONEYLINE and m.selection == game.home_team), None)
            if line is None:
                line = next((m for m in game_markets if m.market_type == MarketType.MONEYLINE), None)
            odds = line.current_odds if line and line.current_odds is not None else -110

            edge = moneyline_edge(probability, odds)["edge"]
            cie = confidence_integrity({"prediction_strength": score, "data_uncertainty": 5, "volatility_penalty": 3, "calibration_penalty": 2})
            dqe = decision_quality({"evidence_quality": 75, "model_agreement": 72, "positive_ev": max(0, min(100, edge*1000)), "simulation_stability": 70, "calibration_support": 65, "explainability": 80})
            lci = luca_composite_intelligence({"upr_edge": score, "cae": score, "mde": score, "gce": 70, "edge": max(0, min(100, 50+edge*500)), "sie": 70, "cie": cie, "mie": 65})

            evaluation = GameEvaluation(
                game=game,
                projected_margin=round((score - 50) / 5, 2),
                moneyline_probability=round(probability, 4),
                best_edge=round(edge, 4),
                module_scores=ModuleScores(scores={**modules, "CIE": cie, "DQE": dqe, "LCI": lci}),
                raw={"odds": odds, "market_count": len(game_markets)},
            )
            evaluations.append(evaluation)

            status = apply_governance(cie, edge, evaluation.risk_grade, .80)
            unit = assign_units(lci, evaluation.risk_grade, edge)
            pick = PickRecommendation(
                category=assign_category(lci),
                sport=self.sport,
                league="Soccer",
                game_id=game.game_id,
                market_type=MarketType.MONEYLINE,
                selection=game.home_team,
                odds=odds,
                confidence=round(cie, 2),
                units=unit.official_units,
                expected_value=round(edge, 4),
                luca_score=round(lci, 2),
                governance_status=status,
                notes=["Phase 2 provider-ready formula output."],
                audit={"modules": modules, "market_count": len(game_markets)},
            )

            if status.value == "approved":
                recommendations.append(pick)
            else:
                pass_list.append({"game_id": game.game_id, "reason": status.value, "edge": edge, "luca_score": round(lci, 2)})

        return LucaRunResult(
            sport=self.sport,
            league="Soccer",
            date=games[0].date if games else "",
            slate_size=len(games),
            games_evaluated=len(games),
            data_completeness=.80 if games else 0.0,
            model_version="1.0.0-phase2",
            evaluations=evaluations,
            recommendations=recommendations,
            pass_list=pass_list,
        )
