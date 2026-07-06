from __future__ import annotations

from luca.intelligence.mlb.environment.models import ParkPhysicsInput, ParkPhysicsOutput


def score_park_physics(row: ParkPhysicsInput) -> ParkPhysicsOutput:
    warnings: list[str] = []

    run_factor = 50 + (row.park_factor_runs - 1.0) * 80
    power_factor = 50 + (row.park_factor_hr - 1.0) * 95
    altitude_boost = min(18, max(0, row.altitude_ft) / 350.0)
    carry = row.wall_carry_score * 0.45 + power_factor * 0.35 + (50 + altitude_boost) * 0.20

    suppression = row.foul_territory_score * 0.35 + (100 - row.surface_speed_score) * 0.20 + (100 - power_factor) * 0.45

    if row.altitude_ft >= 2500:
        warnings.append("Altitude materially supports carry.")
    if row.roof_state.lower() == "closed":
        warnings.append("Closed roof reduces environmental volatility.")

    final = run_factor * 0.34 + power_factor * 0.28 + carry * 0.24 + (100 - suppression) * 0.14

    return ParkPhysicsOutput(
        run_factor_score=round(max(0, min(100, run_factor)), 2),
        power_factor_score=round(max(0, min(100, power_factor)), 2),
        batted_ball_carry_score=round(max(0, min(100, carry)), 2),
        park_suppression_score=round(max(0, min(100, suppression)), 2),
        final_park_score=round(max(0, min(100, final)), 2),
        warnings=warnings,
    )
