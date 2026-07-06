from __future__ import annotations

from luca.intelligence.nfl.skill_coverage.models import CoverageUnitInput, CoverageUnitOutput


def score_coverage_unit(row: CoverageUnitInput) -> CoverageUnitOutput:
    warnings: list[str] = []

    quality = (
        (row.man_coverage_score if row.man_coverage_score is not None else 50.0) * 0.22
        + (row.zone_coverage_score if row.zone_coverage_score is not None else 50.0) * 0.22
        + (row.pressure_coverage_synergy_score if row.pressure_coverage_synergy_score is not None else 50.0) * 0.18
        + (row.safety_help_score if row.safety_help_score is not None else 50.0) * 0.16
        + (row.communication_score if row.communication_score is not None else 50.0) * 0.22
        - row.injury_penalty
    )
    explosive_prevention = (
        (row.explosive_pass_prevention_score if row.explosive_pass_prevention_score is not None else 50.0) * 0.42
        + (row.boundary_coverage_score if row.boundary_coverage_score is not None else 50.0) * 0.20
        + (row.safety_help_score if row.safety_help_score is not None else 50.0) * 0.28
        + quality * 0.10
    )
    flexibility = (
        (row.slot_coverage_score if row.slot_coverage_score is not None else 50.0) * 0.22
        + (row.boundary_coverage_score if row.boundary_coverage_score is not None else 50.0) * 0.22
        + (row.linebacker_coverage_score if row.linebacker_coverage_score is not None else 50.0) * 0.18
        + (row.safety_help_score if row.safety_help_score is not None else 50.0) * 0.20
        + quality * 0.18
    )
    communication = row.communication_score if row.communication_score is not None else 50.0

    if row.injury_penalty >= 8:
        warnings.append("Coverage injury penalty is material.")
    if explosive_prevention < 44:
        warnings.append("Coverage unit has explosive pass vulnerability.")
    if communication < 44:
        warnings.append("Coverage communication risk detected.")

    final = quality * 0.36 + explosive_prevention * 0.26 + flexibility * 0.24 + communication * 0.14

    return CoverageUnitOutput(
        coverage_quality_score=round(max(0, min(100, quality)), 2),
        explosive_prevention_score=round(max(0, min(100, explosive_prevention)), 2),
        matchup_flexibility_score=round(max(0, min(100, flexibility)), 2),
        communication_health_score=round(max(0, min(100, communication)), 2),
        final_coverage_score=round(max(0, min(100, final)), 2),
        warnings=warnings,
    )
