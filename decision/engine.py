from __future__ import annotations

from pydantic import BaseModel

from luca.core.models import GovernanceStatus, MarketType, PickCategory, PickRecommendation, Sport
from luca.ev.engine import ExpectedValueResult, calculate_ev
from luca.governance.engine import apply_governance, assign_category
from luca.risk.engine import RiskInput, RiskResult, calculate_risk
from luca.units.engine import assign_units


class DecisionInput(BaseModel):
    sport: Sport
    league: str
    game_id: str
    market_type: MarketType
    selection: str
    odds: float
    luca_score: float
    projected_probability: float
    confidence: float
    data_completeness: float = 0.80
    variance: float = 1.0
    volatility: float = 0.12


class DecisionOutput(BaseModel):
    pick: PickRecommendation
    ev: ExpectedValueResult
    risk: RiskResult
    governance_status: GovernanceStatus


def make_decision(row: DecisionInput) -> DecisionOutput:
    risk = calculate_risk(RiskInput(
        variance=row.variance,
        data_completeness=row.data_completeness,
        volatility=row.volatility,
    ))
    ev = calculate_ev(row.projected_probability, row.odds, risk_penalty=risk.risk_penalty)
    governance = apply_governance(
        confidence=row.confidence,
        expected_value=ev.risk_adjusted_ev,
        risk_grade=risk.risk_grade,
        data_completeness=row.data_completeness,
    )
    units = assign_units(row.luca_score, risk.risk_grade, ev.risk_adjusted_ev)
    category = assign_category(row.luca_score)

    if governance != GovernanceStatus.APPROVED:
        if ev.tier == "pass":
            category = PickCategory.PASS
        elif risk.risk_grade == "extreme":
            category = PickCategory.AVOID

    pick = PickRecommendation(
        category=category,
        sport=row.sport,
        league=row.league,
        game_id=row.game_id,
        market_type=row.market_type,
        selection=row.selection,
        odds=row.odds,
        confidence=round(row.confidence, 2),
        units=units.official_units,
        expected_value=ev.risk_adjusted_ev,
        luca_score=round(row.luca_score, 2),
        governance_status=governance,
        notes=[
            f"EV tier: {ev.tier}",
            f"Risk grade: {risk.risk_grade}",
            units.reason,
        ],
        audit={
            "ev": ev.model_dump(),
            "risk": risk.model_dump(),
            "unit": units.model_dump(),
        },
    )
    return DecisionOutput(pick=pick, ev=ev, risk=risk, governance_status=governance)
