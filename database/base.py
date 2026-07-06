from abc import ABC, abstractmethod
from typing import Iterable
from luca.ledger.models import LedgerDecision

class LedgerRepository(ABC):
    @abstractmethod
    def add_decision(self, decision: LedgerDecision) -> None: ...
    @abstractmethod
    def list_decisions(self) -> list[LedgerDecision]: ...
    def add_many(self, decisions: Iterable[LedgerDecision]) -> None:
        for d in decisions: self.add_decision(d)
