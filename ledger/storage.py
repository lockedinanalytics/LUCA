import json
from pathlib import Path
from luca.ledger.models import LedgerDecision

class JsonLedgerStore:
    def __init__(self, path: str="luca_ledger.jsonl"):
        self.path = Path(path)
    def append(self, decision: LedgerDecision) -> None:
        with self.path.open("a", encoding="utf-8") as f: f.write(decision.model_dump_json()+"\n")
    def list_all(self) -> list[LedgerDecision]:
        if not self.path.exists(): return []
        return [LedgerDecision.model_validate(json.loads(line)) for line in self.path.read_text(encoding="utf-8").splitlines() if line.strip()]
