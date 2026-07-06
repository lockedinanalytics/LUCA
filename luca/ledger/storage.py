from __future__ import annotations

import json
from pathlib import Path
from typing import List

from luca.ledger.models import LedgerDecision


class JsonLedgerStore:
    def __init__(self, path: str = "luca_ledger.jsonl"):
        self.path = Path(path)

    def append(self, decision: LedgerDecision) -> None:
        with self.path.open("a", encoding="utf-8") as f:
            f.write(decision.model_dump_json() + "\n")

    def list_all(self) -> List[LedgerDecision]:
        if not self.path.exists():
            return []
        records = []
        with self.path.open("r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    records.append(LedgerDecision.model_validate(json.loads(line)))
        return records
