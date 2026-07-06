from __future__ import annotations

from typing import List

from luca.core.models import Sport, TeamGame
from luca.providers.base import ScheduleProvider


class NcaafStaticScheduleProvider(ScheduleProvider):
    def get_games(self, sport: Sport, league: str, date: str) -> List[TeamGame]:
        if sport != Sport.NCAAF:
            return []
        return [TeamGame(game_id=f"ncaaf-{date}-001", sport=Sport.NCAAF, league=league, date=date, away_team="Away College", home_team="Home College", venue="College Stadium")]
