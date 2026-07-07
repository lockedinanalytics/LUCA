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

        payload = self.client.probable_pitchers(date)
        games: list[TeamGame] = []
        for day in payload.get("dates", []):
            for game in day.get("games", []):
                teams = game.get("teams", {})
                away = teams.get("away", {}).get("team", {}).get("name", "Away")
                home = teams.get("home", {}).get("team", {}).get("name", "Home")
                away_probable_obj = teams.get("away", {}).get("probablePitcher", {}) or {}
                home_probable_obj = teams.get("home", {}).get("probablePitcher", {}) or {}

                away_probable = away_probable_obj.get("fullName")
                home_probable = home_probable_obj.get("fullName")

                away_probable_id = away_probable_obj.get("id")
                home_probable_id = home_probable_obj.get("id")
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
                            "away_probable_pitcher_id": away_probable_id,
                            "home_probable_pitcher_id": home_probable_id,
                        },
                    )
                )
        return games
