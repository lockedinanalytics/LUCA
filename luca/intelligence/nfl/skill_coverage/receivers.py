from __future__ import annotations

from luca.intelligence.nfl.skill_coverage.models import ReceiverUnitInput, ReceiverUnitOutput


def score_receiver_unit(row: ReceiverUnitInput) -> ReceiverUnitOutput:
    warnings: list[str] = []

    separation = row.separation_score if row.separation_score is not None else 50.0
    utilization = (
        (row.target_share_score if row.target_share_score is not None else 50.0) * 0.45
        + (row.route_participation_score if row.route_participation_score is not None else 50.0) * 0.35
        + (row.depth_score if row.depth_score is not None else 50.0) * 0.20
    )
    explosive = (
        (row.explosive_route_score if row.explosive_route_score is not None else 50.0) * 0.34
        + (row.yards_after_catch_score if row.yards_after_catch_score is not None else 50.0) * 0.24
        + (row.boundary_efficiency_score if row.boundary_efficiency_score is not None else 50.0) * 0.22
        + separation * 0.20
    )
    possession = (
        (row.contested_catch_score if row.contested_catch_score is not None else 50.0) * 0.28
        + (row.slot_efficiency_score if row.slot_efficiency_score is not None else 50.0) * 0.24
        + separation * 0.25
        + utilization * 0.23
    )
    depth_health = (row.depth_score if row.depth_score is not None else 50.0) - row.injury_penalty

    if row.injury_penalty >= 8:
        warnings.append("Receiver unit injury penalty is material.")
    if separation < 44:
        warnings.append("Receiver separation profile is below average.")
    if utilization < 44:
        warnings.append("Receiver utilization profile is thin.")

    final = separation * 0.24 + utilization * 0.20 + explosive * 0.22 + possession * 0.22 + depth_health * 0.12

    return ReceiverUnitOutput(
        separation_score=round(max(0, min(100, separation)), 2),
        utilization_score=round(max(0, min(100, utilization)), 2),
        explosive_skill_score=round(max(0, min(100, explosive)), 2),
        possession_skill_score=round(max(0, min(100, possession)), 2),
        depth_health_score=round(max(0, min(100, depth_health)), 2),
        final_receiver_score=round(max(0, min(100, final)), 2),
        warnings=warnings,
    )
