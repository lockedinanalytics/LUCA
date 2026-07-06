from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Iterable, List
from luca.ledger.models import LedgerDecision

class LedgerRepository(ABC):
    @abstractmethod
    def add_decision(self, decision: LedgerDecision) -> None:
        raise NotImplementedError

    @abstractmethod
    def list_decisions(self) -> List[LedgerDecision]:
        raise NotImplementedError

    @abstractmethod
    def add_many(self, decisions: Iterable[LedgerDecision]) -> None:
        raise NotImplementedError
