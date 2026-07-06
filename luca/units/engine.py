from __future__ import annotations
from pydantic import BaseModel

class UnitDecision(BaseModel):
    luca_score: float
    risk_grade: str
    expected_value: float | None
    official_units: float
    reason: str

def assign_units(luca_score: float, risk_grade: str="medium", expected_value: float|None=None) -> UnitDecision:
    if expected_value is None or expected_value <= 0:
        return UnitDecision(luca_score=luca_score, risk_grade=risk_grade, expected_value=expected_value, official_units=0.0, reason="No positive EV.")
    cap = .75 if risk_grade.lower() in {"high","extreme"} else 3.0
    units = 3.0 if luca_score >= 92 else 2.0 if luca_score >= 88 else 1.0 if luca_score >= 84 else .5 if luca_score >= 80 else 0.0
    return UnitDecision(luca_score=luca_score, risk_grade=risk_grade, expected_value=expected_value, official_units=min(units, cap), reason="Unit authority applied.")
