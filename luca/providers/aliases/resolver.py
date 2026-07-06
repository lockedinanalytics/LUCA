from __future__ import annotations

from difflib import SequenceMatcher
from pathlib import Path
import json

from luca.providers.aliases.models import TeamAlias


class TeamAliasResolver:
    def __init__(self, aliases: list[TeamAlias] | None = None):
        self.aliases = aliases or load_default_aliases()

    def normalize(self, value: str) -> str:
        return " ".join(value.lower().replace(".", "").replace("-", " ").split())

    def canonicalize(self, name: str, sport: str | None = None, league: str | None = None) -> str:
        target = self.normalize(name)
        best_name = name
        best_score = 0.0

        for row in self.aliases:
            if sport and row.sport and row.sport != sport:
                continue
            if league and row.league and row.league != league:
                continue

            candidates = [row.canonical] + row.aliases
            for candidate in candidates:
                score = SequenceMatcher(None, target, self.normalize(candidate)).ratio()
                if target == self.normalize(candidate):
                    return row.canonical
                if score > best_score:
                    best_score = score
                    best_name = row.canonical

        return best_name if best_score >= 0.86 else name

    def same_team(self, left: str, right: str, sport: str | None = None, league: str | None = None) -> bool:
        return self.canonicalize(left, sport, league) == self.canonicalize(right, sport, league)


def load_default_aliases() -> list[TeamAlias]:
    path = Path(__file__).resolve().parents[2] / "data" / "aliases" / "teams.json"
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    return [TeamAlias(**row) for row in payload]
