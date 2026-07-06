from __future__ import annotations

import json
from pathlib import Path

from luca.market_tracking.models import MarketSnapshot


class JsonMarketSnapshotStore:
    def __init__(self, path: str = "market_snapshots.jsonl"):
        self.path = Path(path)

    def append(self, snapshot: MarketSnapshot) -> None:
        with self.path.open("a", encoding="utf-8") as f:
            f.write(snapshot.model_dump_json() + "\n")

    def list_all(self) -> list[MarketSnapshot]:
        if not self.path.exists():
            return []
        return [
            MarketSnapshot.model_validate(json.loads(line))
            for line in self.path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
