from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from luca.core.models import LucaRunResult, MarketLine, Sport, TeamGame


class SportEngine(ABC):
    sport: Sport

    @abstractmethod
    def evaluate_games(self, games: List[TeamGame], markets: List[MarketLine]) -> LucaRunResult:
        raise NotImplementedError
