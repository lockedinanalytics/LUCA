from __future__ import annotations

from luca.intelligence.nfl.quarterback.models import NflQuarterbackDecisionInput


def score_qb_decision_quality(row: NflQuarterbackDecisionInput) -> tuple[float, list[str]]:
    warnings: list[str] = []
    score = 58.0

    if row.turnover_worthy_play_rate is not None:
        score += (3.2 - row.turnover_worthy_play_rate) * 4.0
    if row.interception_rate is not None:
        score += (2.3 - row.interception_rate) * 3.2
    if row.sack_avoidance_score is not None:
        score = score * 0.75 + row.sack_avoidance_score * 0.25
    if row.checkdown_efficiency_score is not None:
        score = score * 0.88 + row.checkdown_efficiency_score * 0.12
    if row.late_down_decision_score is not None:
        score = score * 0.76 + row.late_down_decision_score * 0.24

    if row.turnover_worthy_play_rate is not None and row.turnover_worthy_play_rate >= 4.5:
        warnings.append("Turnover-worthy play rate is elevated.")
    if row.interception_rate is not None and row.interception_rate >= 3.2:
        warnings.append("Interception rate creates volatility.")

    return round(max(0, min(100, score)), 2), warnings
