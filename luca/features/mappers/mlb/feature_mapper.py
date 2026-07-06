from __future__ import annotations

from typing import Any


class MlbFeatureMapper:
    """
    Converts raw MLB game/provider data into normalized LUCA feature dictionaries.
    This keeps the run engine from depending directly on provider-specific shapes.
    """

    def map_game(self, game: Any) -> dict[str, Any]:
        if isinstance(game, dict):
            return game

        if hasattr(game, "model_dump"):
            return game.model_dump()

        if hasattr(game, "dict"):
            return game.dict()

        return {
            "game_id": getattr(game, "game_id", None),
            "home_team": getattr(game, "home_team", None),
            "away_team": getattr(game, "away_team", None),
            "start_time": getattr(game, "start_time", None),
        }

    def map_games(self, games: list[Any]) -> list[dict[str, Any]]:
        return [self.map_game(game) for game in games]
