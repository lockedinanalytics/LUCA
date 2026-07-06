from __future__ import annotations

from luca.core.models import TeamGame
from luca.providers.weather.models import WeatherSnapshot


class OpenMeteoWeatherProvider:
    """Phase 3 shell.

    Phase 4 should add stadium geocoding and Open-Meteo HTTP calls.
    """

    def get_weather(self, game: TeamGame) -> WeatherSnapshot:
        return WeatherSnapshot(game_id=game.game_id, available=False, source="open_meteo_pending_geocode")
