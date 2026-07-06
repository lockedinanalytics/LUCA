from __future__ import annotations

from pydantic import BaseModel, Field

from luca.core.models import PickRecommendation


class DecisionTrace(BaseModel):
    decision_id: str
    game_id: str
    selection: str
    module_drivers: dict[str, float]
    positive_drivers: list[str]
    negative_drivers: list[str]
    governance_status: str
    unit_reason: str | None = None
    notes: list[str] = Field(default_factory=list)


def build_decision_trace(decision_id: str, pick: PickRecommendation) -> DecisionTrace:
    modules = pick.audit.get("modules", {})
    ordered = sorted(modules.items(), key=lambda item: item[1], reverse=True)
    return DecisionTrace(
        decision_id=decision_id,
        game_id=pick.game_id,
        selection=pick.selection,
        module_drivers=modules,
        positive_drivers=[key for key, value in ordered[:5] if value >= 55],
        negative_drivers=[key for key, value in ordered[-5:] if value <= 48],
        governance_status=pick.governance_status.value,
        unit_reason="Unit authority applied from LUCA score, EV, and risk grade.",
        notes=pick.notes,
    )
