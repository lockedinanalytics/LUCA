from __future__ import annotations

from typing import Any, Dict

from luca.core.models import MarketLine, TeamGame


def build_feature_context(game: TeamGame, markets: list[MarketLine]) -> Dict[str, Any]:
    return {
        "game_id": game.game_id,
        "sport": game.sport.value,
        "league": game.league,
        "home_team": game.home_team,
        "away_team": game.away_team,
        "venue": game.venue,
        "market_count": len([m for m in markets if m.game_id == game.game_id]),
        "data_completeness": 0.80,
    }


def module_scores_from_context(context: Dict[str, Any], defaults: dict[str, float]) -> dict[str, float]:
    scores = dict(defaults)
    if context.get("market_count", 0) <= 0:
        scores["market_edge"] = min(scores.get("market_edge", 50.0), 45.0)
    return scores
