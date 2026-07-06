from __future__ import annotations

from luca.intelligence.nfl.quarterback.decision import score_qb_decision_quality
from luca.intelligence.nfl.quarterback.efficiency import score_qb_efficiency
from luca.intelligence.nfl.quarterback.explosive import score_qb_explosive
from luca.intelligence.nfl.quarterback.matchup import score_qb_matchup
from luca.intelligence.nfl.quarterback.mobility import score_qb_mobility
from luca.intelligence.nfl.quarterback.models import NflQuarterbackIntelligenceInput, NflQuarterbackIntelligenceOutput
from luca.intelligence.nfl.quarterback.pressure import score_qb_pressure
from luca.intelligence.nfl.quarterback.situational import score_qb_situational


def _count_populated(section) -> tuple[int, int]:
    data = section.model_dump()
    return sum(value is not None for value in data.values()), len(data)


def calculate_nfl_quarterback_intelligence(row: NflQuarterbackIntelligenceInput) -> NflQuarterbackIntelligenceOutput:
    warnings: list[str] = []

    efficiency, w = score_qb_efficiency(row.efficiency); warnings.extend(w)
    explosive, w = score_qb_explosive(row.explosive); warnings.extend(w)
    pressure, w = score_qb_pressure(row.pressure); warnings.extend(w)
    decision, w = score_qb_decision_quality(row.decision); warnings.extend(w)
    mobility, w = score_qb_mobility(row.mobility); warnings.extend(w)
    situational, w = score_qb_situational(row.situational); warnings.extend(w)
    matchup, w = score_qb_matchup(row.matchup); warnings.extend(w)

    ceiling = (
        explosive * 0.34
        + efficiency * 0.24
        + mobility * 0.16
        + matchup * 0.16
        + situational * 0.10
    )

    floor = (
        decision * 0.28
        + pressure * 0.22
        + efficiency * 0.22
        + situational * 0.18
        + matchup * 0.10
    )

    volatility = max(0, min(100, abs(ceiling - floor) * 1.35 + max(0, 55 - decision) * 0.35))

    final = (
        efficiency * 0.23
        + explosive * 0.15
        + pressure * 0.16
        + decision * 0.18
        + mobility * 0.08
        + situational * 0.08
        + matchup * 0.12
    )

    populated = 0
    total = 0
    for section in [row.efficiency, row.explosive, row.pressure, row.decision, row.mobility, row.situational, row.matchup]:
        p, t = _count_populated(section)
        populated += p
        total += t
    confidence = 45 + (populated / total) * 45 if total else 45
    if warnings:
        confidence -= min(12, len(warnings) * 1.5)

    explainability = {
        "efficiency": efficiency,
        "explosive": explosive,
        "pressure": pressure,
        "decision": decision,
        "mobility": mobility,
        "situational": situational,
        "matchup": matchup,
        "ceiling": round(ceiling, 2),
        "floor": round(floor, 2),
        "volatility": round(volatility, 2),
    }

    return NflQuarterbackIntelligenceOutput(
        passing_efficiency_score=efficiency,
        explosive_passing_score=explosive,
        pressure_resilience_score=pressure,
        decision_quality_score=decision,
        mobility_score=mobility,
        situational_score=situational,
        matchup_score=matchup,
        ceiling_score=round(max(0, min(100, ceiling)), 2),
        floor_score=round(max(0, min(100, floor)), 2),
        volatility_score=round(max(0, min(100, volatility)), 2),
        final_qb_score=round(max(0, min(100, final)), 2),
        confidence=round(max(0, min(100, confidence)), 2),
        warnings=warnings,
        explainability=explainability,
    )
