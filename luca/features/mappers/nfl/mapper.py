from __future__ import annotations

from typing import Any

from luca.core.models import MarketLine, TeamGame
from luca.features.mappers.base import FeatureMapper
from luca.intelligence.nfl.quarterback.engine import calculate_nfl_quarterback_intelligence
from luca.intelligence.nfl.quarterback.models import NflQuarterbackIntelligenceInput
from luca.intelligence.nfl.trench.matchup import calculate_trench_matchup
from luca.intelligence.nfl.trench.models import TrenchMatchupInput
from luca.intelligence.nfl.skill_coverage.matchup import calculate_skill_coverage_matchup
from luca.intelligence.nfl.skill_coverage.models import SkillCoverageMatchupInput
from luca.intelligence.nfl.context.engine import calculate_nfl_context
from luca.intelligence.nfl.context.models import NflContextInput


class NflFeatureMapper(FeatureMapper):
    def build_modules(self, game: TeamGame, markets: list[MarketLine], context: dict[str, Any] | None = None) -> dict[str, float]:
        context = context or {}

        if context.get("quarterback_v2"):
            qb = calculate_nfl_quarterback_intelligence(NflQuarterbackIntelligenceInput(**context["quarterback_v2"]))
            qb_score = qb.final_qb_score
            explosive_score = qb.explosive_passing_score
            variance_penalty = qb.volatility_score
            pressure_resilience = qb.pressure_resilience_score
        else:
            qb_score = context.get("qb_edge", 55.0)
            explosive_score = context.get("explosive_play_edge", 55.0)
            variance_penalty = 50.0
            pressure_resilience = 50.0

        if context.get("trench_v2"):
            trench_payload = dict(context["trench_v2"])
            trench_payload.setdefault("quarterback_pressure_resilience_score", pressure_resilience)
            trench = calculate_trench_matchup(TrenchMatchupInput(**trench_payload))
            trench_score = trench.final_trench_score
            pressure_score = 100 - trench.pressure_projection_score
            run_edge = trench.rushing_efficiency_projection
        else:
            trench_score = context.get("ol_dl_edge", 55.0)
            pressure_score = context.get("pass_protection_edge", 55.0)
            run_edge = context.get("run_game_edge", 55.0)


        if context.get("skill_coverage_v2"):
            skill_payload = dict(context["skill_coverage_v2"])
            skill_payload.setdefault("quarterback_accuracy_score", qb_score)
            skill_payload.setdefault("pass_protection_score", pressure_score)
            skill = calculate_skill_coverage_matchup(SkillCoverageMatchupInput(**skill_payload))
            skill_score = skill.final_skill_coverage_score
            skill_explosive = skill.explosive_pass_projection
            red_zone_skill = skill.red_zone_skill_score
        else:
            skill_score = context.get("skill_coverage_edge", 55.0)
            skill_explosive = explosive_score
            red_zone_skill = context.get("red_zone_skill", 55.0)


        if context.get("context_v2"):
            nfl_context = calculate_nfl_context(NflContextInput(**context["context_v2"]))
            context_score = nfl_context.final_context_score
            coaching_score = nfl_context.coaching_score
            special_teams_score = nfl_context.special_teams_score
            weather_environment_score = nfl_context.environment_score
            rest_travel_score = nfl_context.situational_score
        else:
            context_score = context.get("context_edge", 55.0)
            coaching_score = context.get("coaching_edge", 55.0)
            special_teams_score = context.get("special_teams_edge", 50.0)
            weather_environment_score = context.get("weather_environment", 50.0)
            rest_travel_score = context.get("rest_travel", 55.0)

        return {
            "qb_edge": qb_score,
            "ol_dl_edge": trench_score,
            "explosive_play_edge": (skill_explosive * 0.50 + explosive_score * 0.30 + run_edge * 0.20),
            "defensive_efficiency_edge": context.get("defensive_efficiency_edge", 55.0),
            "injury_edge": context.get("injury_edge", 55.0),
            "coaching_edge": coaching_score,
            "weather_environment": weather_environment_score,
            "rest_travel": rest_travel_score,
            "market_edge": 55.0 if markets else 45.0,
            "qb_volatility": variance_penalty,
            "pass_protection_edge": pressure_score,
            "run_game_edge": run_edge,
            "skill_coverage_edge": skill_score,
            "red_zone_skill": red_zone_skill,
            "special_teams_edge": special_teams_score,
            "context_edge": context_score,
        }
