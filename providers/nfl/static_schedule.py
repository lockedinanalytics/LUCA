from __future__ import annotations

from typing import List

from luca.core.models import Sport, TeamGame
from luca.providers.base import ScheduleProvider


class NflStaticScheduleProvider(ScheduleProvider):
    def get_games(self, sport: Sport, league: str, date: str) -> List[TeamGame]:
        if sport != Sport.NFL:
            return []
        return [TeamGame(game_id=f"nfl-{date}-001", sport=Sport.NFL, league=league, date=date, away_team="Buffalo Bills", home_team="Kansas City Chiefs", venue="Arrowhead Stadium")]
