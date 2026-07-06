from __future__ import annotations

from typing import Protocol

from luca.intelligence.ncaaf.foundation.models import NcaafGameKey


class NcaafScheduleProvider(Protocol):
    def get_games(self, season: int, week: int) -> list[NcaafGameKey]:
        ...


class StaticNcaafScheduleProvider:
    def get_games(self, season: int, week: int) -> list[NcaafGameKey]:
        return [
            NcaafGameKey(season=season, week=week, game_id=f"{season}-w{week}-uga-osu", home_team_id="uga", away_team_id="osu", neutral_site=True, conference_game=False),
            NcaafGameKey(season=season, week=week, game_id=f"{season}-w{week}-boise-nd", home_team_id="boise", away_team_id="nd", neutral_site=False, conference_game=False),
        ]
