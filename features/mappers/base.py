from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from luca.core.models import MarketLine, TeamGame


class FeatureMapper(ABC):
    @abstractmethod
    def build_modules(self, game: TeamGame, markets: list[MarketLine], context: dict[str, Any] | None = None) -> dict[str, float]:
        raise NotImplementedError
