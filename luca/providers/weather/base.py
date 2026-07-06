from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict

from luca.core.models import TeamGame


class WeatherProvider(ABC):
    @abstractmethod
    def get_weather(self, game: TeamGame) -> Dict[str, Any]:
        raise NotImplementedError


class NullWeatherProvider(WeatherProvider):
    def get_weather(self, game: TeamGame) -> Dict[str, Any]:
        return {
            "game_id": game.game_id,
            "available": False,
            "temperature": None,
            "wind_speed": None,
            "wind_direction": None,
            "precipitation": None,
        }
