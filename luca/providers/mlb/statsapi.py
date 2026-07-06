from __future__ import annotations

from typing import List

from luca.core.models import Sport, TeamGame
from luca.providers.base import ScheduleProvider


class MlbStatsApiScheduleProvider(ScheduleProvider):
    """Production placeholder.

    Wire HTTP calls in deployment. Expected source: MLB Stats API schedule endpoint.
    """

    def get_games(self, sport: Sport, league: str, date: str) -> List[TeamGame]:
        if sport != Sport.MLB:
            return []
        return []
