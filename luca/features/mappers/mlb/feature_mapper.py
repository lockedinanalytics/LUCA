from __future__ import annotations

from typing import Any


class MlbFeatureMapper:
    """
    Converts raw MLB provider data into LUCA's module-ready feature structure.
    """

    def build_modules(self, game: Any) -> dict[str, Any]:
        mapped = self.map_game(game)

        return {
            "game_id": mapped.get("game_id") or mapped.get("id"),
            "home_team": mapped.get("home_team"),
            "away_team": mapped.get("away_team"),
            "start_time": mapped.get("start_time"),

            "pitching": mapped.get("pitching", {}),
            "bullpen": mapped.get("bullpen", {}),
            "offense": mapped.get("offense", {}),
            "defense": mapped.get("defense", {}),
            "environment": mapped.get("environment", {}),
            "market": mapped.get("market", {}),
            "context": mapped.get("context", {}),
        }

    def build_many(self, games: list[Any]) -> list[dict[str, Any]]:
        return [self.build_modules(game) for game in games]

    def map_game(self, game: Any) -> dict[str, Any]:
        if isinstance(game, dict):
            return game

        if hasattr(game, "model_dump"):
            return game.model_dump()

        if hasattr(game, "dict"):
            return game.dict()

        return {
            "game_id": getattr(game, "game_id", None),
            "id": getattr(game, "id", None),
            "home_team": getattr(game, "home_team", None),
            "away_team": getattr(game, "away_team", None),
            "start_time": getattr(game, "start_time", None),
            "pitching": getattr(game, "pitching", {}),
            "bullpen": getattr(game, "bullpen", {}),
            "offense": getattr(game, "offense", {}),
            "defense": getattr(game, "defense", {}),
            "environment": getattr(game, "environment", {}),
            "market": getattr(game, "market", {}),
            "context": getattr(game, "context", {}),
        }

    def map_games(self, games: list[Any]) -> list[dict[str, Any]]:
        return [self.map_game(game) for game in games]
