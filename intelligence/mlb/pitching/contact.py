from __future__ import annotations

from luca.intelligence.mlb.pitching.models import ContactManagementInput, ContactManagementOutput


def score_contact_management(row: ContactManagementInput) -> ContactManagementOutput:
    notes: list[str] = []

    damage = 50.0
    if row.hard_hit_rate is not None:
        damage += (40.0 - row.hard_hit_rate) * 0.85
    if row.barrel_rate is not None:
        damage += (8.0 - row.barrel_rate) * 1.5
    if row.home_run_rate is not None:
        damage += (1.10 - row.home_run_rate) * 8.0

    shape = 50.0
    if row.ground_ball_rate is not None:
        shape += (row.ground_ball_rate - 42.0) * 0.35
    if row.fly_ball_rate is not None and row.fly_ball_rate > 40:
        shape -= (row.fly_ball_rate - 40.0) * 0.30
        notes.append("Fly-ball profile can amplify park/weather risk.")

    regression = 50.0
    if row.xera is not None:
        regression += (4.20 - row.xera) * 4.5
    if row.fip is not None:
        regression += (4.20 - row.fip) * 3.8
    if row.xera is not None and row.fip is not None and abs(row.xera - row.fip) >= 0.75:
        notes.append("xERA/FIP gap indicates regression watch.")

    final = damage * 0.40 + shape * 0.20 + regression * 0.40

    return ContactManagementOutput(
        damage_suppression_score=round(max(0, min(100, damage)), 2),
        batted_ball_shape_score=round(max(0, min(100, shape)), 2),
        regression_score=round(max(0, min(100, regression)), 2),
        final_contact_score=round(max(0, min(100, final)), 2),
        notes=notes,
    )
