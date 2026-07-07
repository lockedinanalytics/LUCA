from __future__ import annotations

from typing import Any

from luca.providers.mlb.client import MlbStatsApiClient


class MlbPlayerStatsProvider:
    def __init__(self):
        self.client = MlbStatsApiClient()

    def get_pitcher_stats(self, pitcher_id: str | int, season: str | int | None = None) -> dict[str, Any]:
        return self.client.player_stats(pitcher_id, season=season)
