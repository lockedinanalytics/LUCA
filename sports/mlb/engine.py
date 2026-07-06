from __future__ import annotations

from typing import List

from luca.analytics.engines import confidence_integrity, decision_quality, luca_composite_intelligence
from luca.core.engine import SportEngine
from luca.core.math_utils import weighted_average
from luca.core.models import GameEvaluation, LucaRunResult, MarketLine, MarketType, ModuleScores, Sport, TeamGame
from luca.decision.engine import DecisionInput, make_decision
from luca.features.mappers.factory import get_feature_mapper
from luca.probability.engine import probability_from_luca_score
from luca.simulation.distributions.score_distribution import ScoreDistributionRequest, simulate_score_distribution
from luca.sports.formulas import SPORT_WEIGHTS

class MlbEngine(SportEngine):
    sport = Sport.MLB

    def evaluate_games(self, games: List[TeamGame], markets: List[MarketLine]) -> LucaRunResult:
        evaluations, recommendations, pass_list = [], [], []
        mapper = get_feature_mapper(self.sport)

        for game in games:
            game_markets = [m for m in markets if m.game_id == game.game_id]
            modules = mapper.build_modules(game=game, markets=game_markets)
            module_score = weighted_average(modules, SPORT_WEIGHTS.get(self.sport.value, {}))

            simulation = simulate_score_distribution(
                ScoreDistributionRequest(
                    game_id=game.game_id,
                    home_mean=max(0.5, 4.2 + (module_score - 50) / 18),
                    away_mean=max(0.5, 4.2 - (module_score - 50) / 24),
                    runs=5000,
                )
            )
            probability = probability_from_luca_score(
                module_score,
                evidence_probability=simulation.home_win_probability,
                volatility=min(0.25, max(0.06, simulation.variance / 100)),
            )

            line = next((m for m in game_markets if m.market_type == MarketType.MONEYLINE and m.selection == game.home_team), None)
            if line is None:
                line = next((m for m in game_markets if m.market_type == MarketType.MONEYLINE), None)
            odds = line.current_odds if line and line.current_odds is not None else -110

            cie = confidence_integrity({
                "prediction_strength": module_score,
                "data_uncertainty": 5,
                "volatility_penalty": min(15, simulation.variance * 0.35),
                "calibration_penalty": 2,
            })
            dqe = decision_quality({
                "evidence_quality": 75,
                "model_agreement": 72,
                "positive_ev": 60,
                "simulation_stability": max(0, 100 - simulation.variance),
                "calibration_support": 65,
                "explainability": 80,
            })
            lci = luca_composite_intelligence({
                "upr_edge": module_score,
                "cae": module_score,
                "mde": module_score,
                "gce": 70,
                "edge": 55,
                "sie": 70,
                "cie": cie,
                "mie": 65,
            })

            decision = make_decision(DecisionInput(
                sport=self.sport,
                league="MLB",
                game_id=game.game_id,
                market_type=MarketType.MONEYLINE,
                selection=game.home_team,
                odds=odds,
                luca_score=lci,
                projected_probability=probability.calibrated_probability,
                confidence=cie,
                data_completeness=.82 if game_markets else .72,
                variance=simulation.variance,
                volatility=probability.confidence_interval_high - probability.calibrated_probability,
            ))

            evaluation = GameEvaluation(
                game=game,
                projected_score=f"{round(simulation.projected_away_score, 1)}-{round(simulation.projected_home_score, 1)}",
                projected_margin=simulation.projected_margin,
                projected_total=simulation.projected_total,
                moneyline_probability=probability.calibrated_probability,
                best_edge=decision.ev.edge,
                risk_grade=decision.risk.risk_grade,
                variance_grade="high" if simulation.variance >= 12 else "medium",
                module_scores=ModuleScores(scores={**modules, "CIE": cie, "DQE": dqe, "LCI": lci}),
                raw={"simulation": simulation.model_dump(), "probability": probability.model_dump(), "decision": decision.model_dump()},
            )
            evaluations.append(evaluation)

            if decision.governance_status.value == "approved":
                recommendations.append(decision.pick)
            else:
                pass_list.append({
                    "game_id": game.game_id,
                    "reason": decision.governance_status.value,
                    "edge": decision.ev.edge,
                    "risk": decision.risk.risk_grade,
                    "luca_score": round(lci, 2),
                })

        return LucaRunResult(
            sport=self.sport,
            league="MLB",
            date=games[0].date if games else "",
            slate_size=len(games),
            games_evaluated=len(games),
            data_completeness=.82 if games else 0.0,
            model_version="1.0.0-phase6",
            evaluations=evaluations,
            recommendations=recommendations,
            pass_list=pass_list,
        )
