from __future__ import annotations

from typing import Any


class MlbFeatureMapper:
    """
    Converts raw MLB provider data into LUCA's normalized feature structure.
    """

    def build_modules(
        self,
        game: Any,
        markets: Any | None = None,
        **kwargs: Any,
    ) -> dict[str, float]:
        mapped = self.map_game(game)

        return {
            "pitching": self._score(mapped.get("pitching"), default=50.0),
            "bullpen": self._score(mapped.get("bullpen"), default=50.0),
            "offense": self._score(mapped.get("offense"), default=50.0),
            "defense": self._score(mapped.get("defense"), default=50.0),
            "environment": self._score(mapped.get("environment"), default=50.0),
            "market": self._score(mapped.get("market") or markets, default=50.0),
            "context": self._score(mapped.get("context"), default=50.0),
        }

    def _score(self, value: Any, default: float = 50.0) -> float:
        if value is None:
            return default

        if isinstance(value, (int, float)):
            return float(value)

        if isinstance(value, dict):
            for key in ("score", "value", "rating", "confidence"):
                if key in value and isinstance(value[key], (int, float)):
                    return float(value[key])
            return default

        if isinstance(value, list):
            return default

        if hasattr(value, "score"):
            score = getattr(value, "score")
            if isinstance(score, (int, float)):
                return float(score)

        return default

    def build_many(self, games: list[Any]) -> list[dict[str, float]]:
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
