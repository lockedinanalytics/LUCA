from __future__ import annotations

from luca.intelligence.mlb.defense.models import FieldingUnitInput, FieldingUnitOutput


def score_fielding_unit(row: FieldingUnitInput) -> FieldingUnitOutput:
    warnings: list[str] = []

    infield = (
        row.infield_oaa_score * 0.36
        + row.double_play_score * 0.24
        + row.range_score * 0.18
        + row.error_avoidance_score * 0.14
        + row.positioning_score * 0.08
    )
    outfield = (
        row.outfield_oaa_score * 0.42
        + row.range_score * 0.22
        + row.arm_strength_score * 0.18
        + row.positioning_score * 0.18
    )
    throwing = row.arm_strength_score * 0.55 + row.double_play_score * 0.25 + row.error_avoidance_score * 0.20
    conversion = (
        row.infield_oaa_score * 0.25
        + row.outfield_oaa_score * 0.25
        + row.drs_score * 0.25
        + row.positioning_score * 0.15
        + row.error_avoidance_score * 0.10
    )

    if row.error_avoidance_score < 43:
        warnings.append("Defensive error risk is elevated.")
    if row.outfield_oaa_score < 44:
        warnings.append("Outfield range support below average.")

    final = infield * 0.30 + outfield * 0.27 + throwing * 0.13 + conversion * 0.30

    return FieldingUnitOutput(
        infield_support_score=round(max(0, min(100, infield)), 2),
        outfield_support_score=round(max(0, min(100, outfield)), 2),
        throwing_support_score=round(max(0, min(100, throwing)), 2),
        conversion_score=round(max(0, min(100, conversion)), 2),
        final_fielding_score=round(max(0, min(100, final)), 2),
        warnings=warnings,
    )
