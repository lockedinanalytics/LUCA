from __future__ import annotations

from pydantic import BaseModel


class RiskInput(BaseModel):
    variance: float = 1.0
    data_completeness: float = 0.8
    volatility: float = 0.12
    injury_uncertainty: float = 0.0
    market_disagreement: float = 0.0


class RiskResult(BaseModel):
    risk_score: float
    risk_grade: str
    risk_penalty: float
    notes: list[str]


def calculate_risk(row: RiskInput) -> RiskResult:
    notes = []
    score = 35.0

    score += min(20, row.variance * 2.0)
    score += min(20, row.volatility * 100 * 0.45)
    score += min(15, row.injury_uncertainty)
    score += min(15, row.market_disagreement)

    if row.data_completeness < 0.70:
        score += 15
        notes.append("Data completeness below governance threshold.")
    elif row.data_completeness < 0.85:
        score += 5
        notes.append("Data completeness acceptable but not optimal.")

    if score >= 75:
        grade = "extreme"
        penalty = 0.06
    elif score >= 60:
        grade = "high"
        penalty = 0.035
    elif score >= 45:
        grade = "medium"
        penalty = 0.015
    else:
        grade = "low"
        penalty = 0.005

    return RiskResult(risk_score=round(min(100, score), 2), risk_grade=grade, risk_penalty=penalty, notes=notes)
