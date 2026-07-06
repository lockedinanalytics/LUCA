from __future__ import annotations

from luca.intelligence.mlb.defense.models import BaserunnerPreventionInput, BaserunnerPreventionOutput


def score_baserunner_prevention(row: BaserunnerPreventionInput) -> BaserunnerPreventionOutput:
    warnings: list[str] = []

    steal_prevention = (
        row.catcher_throwing_score * 0.45
        + row.pitcher_hold_score * 0.35
        + row.infield_tag_score * 0.20
    )

    extra_base = (
        row.outfield_arm_score * 0.38
        + row.infield_tag_score * 0.20
        + row.catcher_throwing_score * 0.16
        + row.pitcher_hold_score * 0.10
        + (100 - row.opponent_extra_base_pressure_score) * 0.16
    )

    pressure = (
        steal_prevention * 0.42
        + extra_base * 0.42
        + (100 - row.opponent_steal_pressure_score) * 0.16
    )

    if row.opponent_steal_pressure_score >= 62 and steal_prevention < 50:
        warnings.append("Opponent steal pressure can stress battery.")
    if row.opponent_extra_base_pressure_score >= 62 and extra_base < 50:
        warnings.append("Opponent extra-base pressure can stress outfield arms.")

    return BaserunnerPreventionOutput(
        steal_prevention_score=round(max(0, min(100, steal_prevention)), 2),
        extra_base_prevention_score=round(max(0, min(100, extra_base)), 2),
        pressure_adjusted_score=round(max(0, min(100, pressure)), 2),
        warnings=warnings,
    )
