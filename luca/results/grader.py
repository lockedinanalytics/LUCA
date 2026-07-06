from __future__ import annotations

from typing import Optional
from pydantic import BaseModel

from luca.ledger.models import LedgerDecision


class FinalResult(BaseModel):
    game_id: str
    final_score: str
    winner: Optional[str] = None
    margin: Optional[float] = None
    total: Optional[float] = None
    closing_odds: Optional[float] = None


class GradedDecision(BaseModel):
    decision_id: str
    result: str
    units_won_lost: float
    final_score: str
    audit_status: str = "graded"


def grade_decision(decision: LedgerDecision, final: FinalResult) -> GradedDecision:
    """Initial universal grading shell.

    Production grading will branch by market type. This version handles a basic
    selection-vs-winner result for moneyline-like decisions.
    """
    if final.winner is None:
        result = "pending"
        units = 0.0
    elif decision.selection == final.winner:
        result = "win"
        units = _profit_units(decision.odds, decision.units)
    else:
        result = "loss"
        units = -abs(decision.units)

    return GradedDecision(
        decision_id=decision.decision_id,
        result=result,
        units_won_lost=round(units, 4),
        final_score=final.final_score,
        audit_status="graded" if result in {"win", "loss"} else "pending",
    )


def _profit_units(odds: float | None, units: float) -> float:
    if odds is None:
        return units
    if odds < 0:
        return units * (100.0 / abs(odds))
    return units * (odds / 100.0)
