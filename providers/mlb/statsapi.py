from __future__ import annotations

from typing import List

from luca.core.models import Sport, TeamGame
from luca.providers.base import ScheduleProvider
from luca.providers.mlb.client import MlbStatsApiClient


class MlbStatsApiScheduleProvider(ScheduleProvider):
    def __init__(self):
        self.client = MlbStatsApiClient()

    def get_games(self, sport: Sport, league: str, date: str) -> List[TeamGame]:
        if sport != Sport.MLB:
            return []

        payload = self.client.schedule(date)
        games: list[TeamGame] = []
        for day in payload.get("dates", []):
            for game in day.get("games", []):
                teams = game.get("teams", {})
                away = teams.get("away", {}).get("team", {}).get("name", "Away")
                home = teams.get("home", {}).get("team", {}).get("name", "Home")
                away_probable = teams.get("away", {}).get("probablePitcher", {}).get("fullName")
                home_probable = teams.get("home", {}).get("probablePitcher", {}).get("fullName")
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
                        metadata={
                            "status": game.get("status", {}),
                            "away_probable_pitcher": away_probable,
                            "home_probable_pitcher": home_probable,
                        },
                    )
                )
        return games
