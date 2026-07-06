from __future__ import annotations

from typing import List
import httpx

from luca.config.settings import get_settings
from luca.core.models import Sport, TeamGame
from luca.providers.base import ScheduleProvider
from luca.providers.exceptions import ProviderNetworkDisabled


class MlbStatsApiScheduleProvider(ScheduleProvider):
    def __init__(self):
        self.settings = get_settings()

    def get_games(self, sport: Sport, league: str, date: str) -> List[TeamGame]:
        if sport != Sport.MLB:
            return []
        if not self.settings.allow_live_network_calls:
            raise ProviderNetworkDisabled("Live MLB schedule calls disabled. Set ALLOW_LIVE_NETWORK_CALLS=true.")

        url = f"{self.settings.mlb_stats_api_base_url}/schedule"
        params = {"sportId": 1, "date": date}

        with httpx.Client(timeout=self.settings.provider_timeout_seconds) as client:
            response = client.get(url, params=params)
            response.raise_for_status()
            payload = response.json()

        games: list[TeamGame] = []
        for day in payload.get("dates", []):
            for game in day.get("games", []):
                teams = game.get("teams", {})
                away = teams.get("away", {}).get("team", {}).get("name", "Away")
                home = teams.get("home", {}).get("team", {}).get("name", "Home")
                games.append(
                    TeamGame(
                        game_id=str(game.get("gamePk")),
                        sport=Sport.MLB,
                        league=league,
                        date=date,
                        away_team=away,
                        home_team=home,
                        start_time=game.get("gameDate"),
                        venue=game.get("venue", {}).get("name"),
                        metadata={"status": game.get("status", {})},
                    )
                )
        return games
