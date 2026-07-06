from __future__ import annotations

from typing import List

from luca.analytics.engines import confidence_integrity, decision_quality, luca_composite_intelligence
from luca.core.engine import SportEngine
from luca.core.math_utils import logistic, weighted_average
from luca.core.models import (
    GameEvaluation,
    LucaRunResult,
    MarketLine,
    MarketType,
    ModuleScores,
    PickRecommendation,
    Sport,
    TeamGame,
)
from luca.governance.engine import apply_governance, assign_category, recommended_units
from luca.objectives.engines import moneyline_edge
from luca.sports.formulas import SPORT_WEIGHTS


class NcaafEngine(SportEngine):
    sport = Sport.NCAAF

    def evaluate_games(self, games: List[TeamGame], markets: List[MarketLine]) -> LucaRunResult:
        evaluations: list[GameEvaluation] = []
        recommendations: list[PickRecommendation] = []
        pass_list: list[dict] = []

        for game in games:
            modules = self.default_modules(game)
            sport_score = self.score_from_modules(modules)
            projected_probability = self.probability_from_score(sport_score)

            ml = next(
                (m for m in markets if m.game_id == game.game_id and m.market_type == MarketType.MONEYLINE),
                None,
            )
            edge_data = moneyline_edge(projected_probability, ml.current_odds if ml and ml.current_odds else -110)
            expected_value = edge_data["edge"]

            cie = confidence_integrity({
                "prediction_strength": sport_score,
                "data_uncertainty": 5.0,
                "volatility_penalty": 3.0,
                "calibration_penalty": 2.0,
                "contradiction_penalty": 0.0,
            })
            dqe = decision_quality({
                "evidence_quality": 75,
                "model_agreement": 72,
                "positive_ev": max(0, min(100, expected_value * 1000)),
                "simulation_stability": 70,
                "calibration_support": 65,
                "explainability": 80,
            })
            lci = luca_composite_intelligence({
                "upr_edge": sport_score,
                "cae": sport_score,
                "mde": sport_score,
                "gce": 70,
                "edge": max(0, min(100, 50 + expected_value * 500)),
                "sie": 70,
                "cie": cie,
                "mie": 65,
            })

            evaluation = GameEvaluation(
                game=game,
                projected_margin=round((sport_score - 50) / 5, 2),
                projected_total=None,
                moneyline_probability=round(projected_probability, 4),
                best_edge=round(expected_value, 4),
                risk_grade="medium",
                variance_grade="medium",
                module_scores=ModuleScores(scores={**modules, "CIE": cie, "DQE": dqe, "LCI": lci}),
                raw={"edge_data": edge_data},
            )
            evaluations.append(evaluation)

            status = apply_governance(
                confidence=cie,
                expected_value=expected_value,
                risk_grade=evaluation.risk_grade,
                data_completeness=0.80,
            )

            luca_score = round(lci, 2)
            category = assign_category(luca_score)
            units = recommended_units(luca_score, evaluation.risk_grade)

            pick = PickRecommendation(
                category=category,
                sport=self.sport,
                league="NCAAF",
                game_id=game.game_id,
                market_type=MarketType.MONEYLINE,
                selection=game.home_team,
                odds=ml.current_odds if ml and ml.current_odds else -110,
                confidence=round(cie, 2),
                units=units,
                expected_value=round(expected_value, 4),
                luca_score=luca_score,
                governance_status=status,
                publication_status="internal",
                notes=["Formula-ready sample output until live providers are connected."],
                audit={"modules": modules, "edge_data": edge_data},
            )

            if status.value == "approved":
                recommendations.append(pick)
            else:
                pass_list.append({
                    "game_id": game.game_id,
                    "selection": game.home_team,
                    "reason": status.value,
                    "luca_score": luca_score,
                    "edge": expected_value,
                })

        return LucaRunResult(
            sport=self.sport,
            league="NCAAF",
            date=games[0].date if games else "",
            slate_size=len(games),
            games_evaluated=len(games),
            data_completeness=0.80 if games else 0.0,
            run_status="ok",
            evaluations=evaluations,
            recommendations=recommendations,
            pass_list=pass_list,
        )

    def score_from_modules(self, modules: dict[str, float]) -> float:
        weights = SPORT_WEIGHTS.get(self.sport.value, {})
        return weighted_average(modules, weights)

    def probability_from_score(self, score: float) -> float:
        return logistic((score - 50.0) / 12.0)

    def default_modules(self, game: TeamGame) -> dict[str, float]:
        weights = SPORT_WEIGHTS.get(self.sport.value, {})
        if not weights:
            return {"generic_power": 55.0, "market_edge": 50.0}
        return {key: 55.0 for key in weights}
