from luca.database.base import LedgerRepository
from luca.ledger.models import LedgerDecision
from luca.ledger.storage import JsonLedgerStore

class JsonLedgerRepository(LedgerRepository):
    def __init__(self, path: str="luca_ledger.jsonl"): self.store=JsonLedgerStore(path)
    def add_decision(self, decision: LedgerDecision) -> None: self.store.append(decision)
    def list_decisions(self) -> list[LedgerDecision]: return self.store.list_all()
