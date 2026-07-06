from __future__ import annotations

from typing import Any
import httpx

from luca.config.settings import get_settings
from luca.providers.exceptions import ProviderConfigurationError, ProviderNetworkDisabled


class TheOddsApiClient:
    def __init__(self):
        self.settings = get_settings()
        if not self.settings.odds_api_key:
            raise ProviderConfigurationError("ODDS_API_KEY is not configured.")
        if not self.settings.allow_live_network_calls:
            raise ProviderNetworkDisabled("Live network calls are disabled. Set ALLOW_LIVE_NETWORK_CALLS=true to enable.")
        self.client = httpx.Client(timeout=self.settings.provider_timeout_seconds)

    def get_sports(self) -> list[dict[str, Any]]:
        url = f"{self.settings.odds_api_base_url}/sports"
        response = self.client.get(url, params={"apiKey": self.settings.odds_api_key})
        response.raise_for_status()
        return response.json()

    def get_odds(self, sport_key: str) -> list[dict[str, Any]]:
        url = f"{self.settings.odds_api_base_url}/sports/{sport_key}/odds"
        params = {
            "apiKey": self.settings.odds_api_key,
            "regions": self.settings.odds_api_regions,
            "markets": self.settings.odds_api_markets,
            "oddsFormat": self.settings.odds_api_odds_format,
            "dateFormat": self.settings.odds_api_date_format,
        }
        response = self.client.get(url, params=params)
        response.raise_for_status()
        return response.json()
