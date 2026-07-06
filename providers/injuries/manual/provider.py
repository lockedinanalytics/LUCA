from __future__ import annotations

from pathlib import Path
import json

from luca.core.models import TeamGame


class ManualInjuryProvider:
    def __init__(self, path: str = "manual_injuries.json"):
        self.path = Path(path)

    def get_injuries(self, game: TeamGame) -> dict:
        if not self.path.exists():
            return {"game_id": game.game_id, "available": False, "injuries": []}
        payload = json.loads(self.path.read_text(encoding="utf-8"))
        return payload.get(game.game_id, {"game_id": game.game_id, "available": False, "injuries": []})
