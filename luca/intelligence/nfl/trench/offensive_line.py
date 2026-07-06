from __future__ import annotations

from luca.intelligence.nfl.trench.models import OffensiveLineInput, OffensiveLineOutput


def score_offensive_line(row: OffensiveLineInput) -> OffensiveLineOutput:
    warnings: list[str] = []

    pass_pro = 50.0
    if row.pass_block_win_rate is not None:
        pass_pro += (row.pass_block_win_rate - 60.0) * 0.75
    if row.pressure_allowed_rate is not None:
        pass_pro += (32.0 - row.pressure_allowed_rate) * 0.75
    if row.sack_responsibility_rate is not None:
        pass_pro += (7.0 - row.sack_responsibility_rate) * 1.4
    if row.blitz_pickup_score is not None:
        pass_pro = pass_pro * 0.78 + row.blitz_pickup_score * 0.22
    if row.interior_protection_score is not None:
        pass_pro = pass_pro * 0.88 + row.interior_protection_score * 0.12
    if row.edge_protection_score is not None:
        pass_pro = pass_pro * 0.86 + row.edge_protection_score * 0.14

    run_block = 50.0
    if row.run_block_win_rate is not None:
        run_block += (row.run_block_win_rate - 70.0) * 0.65
    if row.short_yardage_score is not None:
        run_block = run_block * 0.84 + row.short_yardage_score * 0.16
    if row.goal_line_blocking_score is not None:
        run_block = run_block * 0.88 + row.goal_line_blocking_score * 0.12

    continuity = 50.0
    if row.continuity_score is not None:
        continuity = continuity * 0.55 + row.continuity_score * 0.45
    if row.depth_quality_score is not None:
        continuity = continuity * 0.75 + row.depth_quality_score * 0.25
    continuity -= row.injury_penalty
    continuity -= row.fatigue_penalty

    short_yardage = (
        (row.short_yardage_score if row.short_yardage_score is not None else 50.0) * 0.55
        + (row.goal_line_blocking_score if row.goal_line_blocking_score is not None else 50.0) * 0.45
    )

    if row.pressure_allowed_rate is not None and row.pressure_allowed_rate >= 38:
        warnings.append("Offensive line pressure allowed rate is elevated.")
    if row.injury_penalty >= 8:
        warnings.append("Offensive line injury penalty is material.")
    if row.continuity_score is not None and row.continuity_score < 44:
        warnings.append("Offensive line continuity is weak.")

    final = pass_pro * 0.36 + run_block * 0.28 + continuity * 0.18 + short_yardage * 0.18

    return OffensiveLineOutput(
        pass_protection_score=round(max(0, min(100, pass_pro)), 2),
        run_blocking_score=round(max(0, min(100, run_block)), 2),
        continuity_health_score=round(max(0, min(100, continuity)), 2),
        short_yardage_score=round(max(0, min(100, short_yardage)), 2),
        final_ol_score=round(max(0, min(100, final)), 2),
        warnings=warnings,
    )
