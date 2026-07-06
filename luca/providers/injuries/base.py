from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict

from luca.core.models import TeamGame


class InjuryProvider(ABC):
    @abstractmethod
    def get_injuries(self, game: TeamGame) -> Dict[str, Any]:
        raise NotImplementedError


class NullInjuryProvider(InjuryProvider):
    def get_injuries(self, game: TeamGame) -> Dict[str, Any]:
        return {"game_id": game.game_id, "available": False, "injuries": []}
