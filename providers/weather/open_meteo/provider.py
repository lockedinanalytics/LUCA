from __future__ import annotations

import httpx

from luca.config.settings import get_settings
from luca.core.models import TeamGame
from luca.providers.exceptions import ProviderNetworkDisabled
from luca.providers.venues.resolver import VenueResolver
from luca.providers.weather.models import WeatherSnapshot


class OpenMeteoWeatherProvider:
    def __init__(self):
        self.settings = get_settings()
        self.venue_resolver = VenueResolver()

    def get_weather(self, game: TeamGame) -> WeatherSnapshot:
        venue = self.venue_resolver.resolve(game.venue, game.home_team)
        if venue is None:
            return WeatherSnapshot(game_id=game.game_id, available=False, source="open_meteo", warnings=["Venue coordinates unavailable."])

        if not self.settings.allow_live_network_calls:
            return WeatherSnapshot(game_id=game.game_id, available=False, source="open_meteo", warnings=["Live weather calls disabled."])

        params = {
            "latitude": venue.latitude,
            "longitude": venue.longitude,
            "current": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m,wind_direction_10m",
            "temperature_unit": "fahrenheit",
            "wind_speed_unit": "mph",
            "precipitation_unit": "inch",
        }

        with httpx.Client(timeout=self.settings.provider_timeout_seconds) as client:
            response = client.get("https://api.open-meteo.com/v1/forecast", params=params)
            response.raise_for_status()
            payload = response.json()

        current = payload.get("current", {})
        return WeatherSnapshot(
            game_id=game.game_id,
            available=True,
            temperature_f=current.get("temperature_2m"),
            wind_speed_mph=current.get("wind_speed_10m"),
            wind_direction_degrees=current.get("wind_direction_10m"),
            precipitation_probability=current.get("precipitation"),
            humidity=current.get("relative_humidity_2m"),
            source="open_meteo",
        )
