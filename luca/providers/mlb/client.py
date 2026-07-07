from __future__ import annotations

import httpx

from luca.config.settings import get_settings
from luca.providers.exceptions import ProviderNetworkDisabled


class MlbStatsApiClient:
    def __init__(self):
        self.settings = get_settings()

    def _get(self, path: str, params: dict | None = None) -> dict:
        if not self.settings.allow_live_network_calls:
            raise ProviderNetworkDisabled(
                "Live MLB calls disabled. Set ALLOW_LIVE_NETWORK_CALLS=true."
            )

        url = f"{self.settings.mlb_stats_api_base_url}{path}"

        with httpx.Client(timeout=self.settings.provider_timeout_seconds) as client:
            response = client.get(url, params=params or {})
            response.raise_for_status()
            return response.json()

    def schedule(self, date: str) -> dict:
        return self._get("/schedule", {"sportId": 1, "date": date})

    def boxscore(self, game_pk: str | int) -> dict:
        return self._get(f"/game/{game_pk}/boxscore")

    def linescore(self, game_pk: str | int) -> dict:
        return self._get(f"/game/{game_pk}/linescore")

    def probable_pitchers(self, date: str) -> dict:
        return self._get(
            "/schedule",
            {"sportId": 1, "date": date, "hydrate": "probablePitcher"},
        )

    def player_stats(self, player_id: str | int, season: str | int | None = None) -> dict:
        params = {
            "hydrate": "stats(group=[pitching],type=[season])"
        }

        if season is not None:
            params["season"] = str(season)

        return self._get(f"/people/{player_id}", params)
