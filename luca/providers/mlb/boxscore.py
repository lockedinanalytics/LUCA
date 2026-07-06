from __future__ import annotations

from typing import Any

from luca.providers.mlb.client import MlbStatsApiClient


class MlbBoxscoreProvider:
    def __init__(self):
        self.client = MlbStatsApiClient()

    def get_boxscore(self, game_id: str) -> dict[str, Any]:
        return self.client.boxscore(game_id)

    def extract_lineup_names(self, boxscore: dict, side: str) -> list[str]:
        team = boxscore.get("teams", {}).get(side, {})
        batters = team.get("batters", [])
        players = team.get("players", {})
        names = []
        for player_id in batters:
            key = f"ID{player_id}"
            player = players.get(key, {})
            person = player.get("person", {})
            if person.get("fullName"):
                names.append(person["fullName"])
        return names
