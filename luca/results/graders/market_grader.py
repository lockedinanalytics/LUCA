from __future__ import annotations

from luca.ledger.models import LedgerDecision
from luca.results.grader import FinalResult, GradedDecision


def grade_by_market(decision: LedgerDecision, final: FinalResult) -> GradedDecision:
    market = decision.market.lower()

    if market == "moneyline":
        return _grade_moneyline(decision, final)

    if market == "spread":
        return _grade_spread(decision, final)

    if market == "total":
        return _grade_total(decision, final)

    return GradedDecision(
        decision_id=decision.decision_id,
        result="pending",
        units_won_lost=0.0,
        final_score=final.final_score,
        audit_status="unsupported_market",
    )


def _grade_moneyline(decision: LedgerDecision, final: FinalResult) -> GradedDecision:
    if final.winner is None:
        result, units = "pending", 0.0
    elif decision.selection == final.winner:
        result, units = "win", _profit_units(decision.odds, decision.units)
    else:
        result, units = "loss", -abs(decision.units)
    return GradedDecision(decision_id=decision.decision_id, result=result, units_won_lost=round(units, 4), final_score=final.final_score)


def _grade_spread(decision: LedgerDecision, final: FinalResult) -> GradedDecision:
    if final.margin is None:
        return GradedDecision(decision_id=decision.decision_id, result="pending", units_won_lost=0.0, final_score=final.final_score)
    spread = decision.module_snapshot.get("published_spread")
    if spread is None:
        return GradedDecision(decision_id=decision.decision_id, result="pending", units_won_lost=0.0, final_score=final.final_score, audit_status="missing_spread")
    covered_value = final.margin + float(spread)
    if covered_value > 0:
        result, units = "win", _profit_units(decision.odds, decision.units)
    elif covered_value < 0:
        result, units = "loss", -abs(decision.units)
    else:
        result, units = "push", 0.0
    return GradedDecision(decision_id=decision.decision_id, result=result, units_won_lost=round(units, 4), final_score=final.final_score)


def _grade_total(decision: LedgerDecision, final: FinalResult) -> GradedDecision:
    if final.total is None:
        return GradedDecision(decision_id=decision.decision_id, result="pending", units_won_lost=0.0, final_score=final.final_score)
    market_total = decision.module_snapshot.get("published_total")
    side = decision.selection.lower()
    if market_total is None:
        return GradedDecision(decision_id=decision.decision_id, result="pending", units_won_lost=0.0, final_score=final.final_score, audit_status="missing_total")
    diff = final.total - float(market_total)
    if diff == 0:
        result, units = "push", 0.0
    elif (side == "over" and diff > 0) or (side == "under" and diff < 0):
        result, units = "win", _profit_units(decision.odds, decision.units)
    else:
        result, units = "loss", -abs(decision.units)
    return GradedDecision(decision_id=decision.decision_id, result=result, units_won_lost=round(units, 4), final_score=final.final_score)


def _profit_units(odds: float | None, units: float) -> float:
    if odds is None:
        return units
    if odds < 0:
        return units * (100.0 / abs(odds))
    return units * (odds / 100.0)
