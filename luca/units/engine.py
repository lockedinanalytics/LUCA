from __future__ import annotations

from pydantic import BaseModel


class UnitDecision(BaseModel):
    luca_score: float
    risk_grade: str
    expected_value: float | None
    official_units: float
    reason: str


def assign_units(luca_score: float, risk_grade: str = "medium", expected_value: float | None = None) -> UnitDecision:
    if expected_value is None or expected_value <= 0:
        return UnitDecision(luca_score=luca_score, risk_grade=risk_grade, expected_value=expected_value, official_units=0.0, reason="No positive EV.")

    risk = risk_grade.lower()
    cap = 0.75 if risk in {"high", "extreme"} else 3.0

    if luca_score >= 92:
        units = 3.0
    elif luca_score >= 88:
        units = 2.0
    elif luca_score >= 84:
        units = 1.0
    elif luca_score >= 80:
        units = 0.5
    else:
        units = 0.0

    units = min(units, cap)
    return UnitDecision(luca_score=luca_score, risk_grade=risk_grade, expected_value=expected_value, official_units=units, reason="Unit authority applied.")
