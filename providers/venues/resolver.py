from __future__ import annotations

from pathlib import Path
import json
from difflib import SequenceMatcher

from luca.providers.venues.models import VenueLocation


class VenueResolver:
    def __init__(self, venues: list[VenueLocation] | None = None):
        self.venues = venues or load_mlb_venues()

    def normalize(self, value: str) -> str:
        return " ".join(value.lower().replace(".", "").replace("-", " ").split())

    def resolve(self, venue_name: str | None = None, team: str | None = None) -> VenueLocation | None:
        if not venue_name and not team:
            return None

        candidates = []
        for venue in self.venues:
            scores = []
            if venue_name:
                scores.append(SequenceMatcher(None, self.normalize(venue_name), self.normalize(venue.name)).ratio())
            if team and venue.team:
                scores.append(SequenceMatcher(None, self.normalize(team), self.normalize(venue.team)).ratio())
            if scores:
                candidates.append((max(scores), venue))

        if not candidates:
            return None

        score, venue = max(candidates, key=lambda row: row[0])
        return venue if score >= 0.80 else None


def load_mlb_venues() -> list[VenueLocation]:
    path = Path(__file__).resolve().parents[2] / "data" / "venues" / "mlb_venues.json"
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    return [VenueLocation(**row) for row in payload]
