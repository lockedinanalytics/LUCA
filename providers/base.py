from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
from luca.core.models import MarketLine, Sport, TeamGame

class ScheduleProvider(ABC):
    @abstractmethod
    def get_games(self, sport: Sport, league: str, date: str) -> List[TeamGame]:
        raise NotImplementedError

class MarketProvider(ABC):
    @abstractmethod
    def get_markets(self, games: List[TeamGame]) -> List[MarketLine]:
        raise NotImplementedError
