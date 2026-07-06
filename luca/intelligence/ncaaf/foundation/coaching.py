from __future__ import annotations

from luca.intelligence.ncaaf.foundation.models import CoachingContinuityInput


def score_coaching_continuity(row: CoachingContinuityInput) -> tuple[float, list[str]]:
    warnings: list[str] = []
    score = (
        row.head_coach_continuity_score * 0.25
        + row.offensive_coordinator_continuity_score * 0.19
        + row.defensive_coordinator_continuity_score * 0.19
        + row.scheme_stability_score * 0.20
        + row.historical_system_performance_score * 0.17
        - row.staff_turnover_penalty
    )
    if row.staff_turnover_penalty >= 8:
        warnings.append("Staff turnover penalty is material.")
    if row.scheme_stability_score < 42:
        warnings.append("Scheme stability risk.")
    return round(max(0, min(100, score)), 2), warnings
