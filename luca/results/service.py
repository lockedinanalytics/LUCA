from __future__ import annotations

from luca.database.base import LedgerRepository
from luca.results.grader import FinalResult, GradedDecision, grade_decision


def grade_game_decisions(repository: LedgerRepository, final: FinalResult) -> list[GradedDecision]:
    decisions = [d for d in repository.list_decisions() if d.game_id == final.game_id]
    return [grade_decision(decision, final) for decision in decisions]
