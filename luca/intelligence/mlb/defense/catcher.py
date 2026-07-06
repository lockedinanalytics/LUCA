from __future__ import annotations

from luca.intelligence.mlb.defense.models import CatcherInput, CatcherOutput


def score_catcher(row: CatcherInput) -> CatcherOutput:
    warnings: list[str] = []

    receiving = row.framing_score * 0.55 + row.blocking_score * 0.25 + row.game_calling_score * 0.20
    run_game = row.throwing_score * 0.45 + row.pop_time_score * 0.35 + row.blocking_score * 0.20
    pitcher_support = row.game_calling_score * 0.40 + row.pitcher_familiarity_score * 0.35 + row.framing_score * 0.25

    fatigue_adjusted = (
        receiving * 0.35
        + run_game * 0.25
        + pitcher_support * 0.30
        + row.workload_fatigue_score * 0.10
        - row.availability_penalty
    )

    if row.availability_penalty >= 8:
        warnings.append(f"{row.name}: availability penalty applied.")
    if row.workload_fatigue_score < 42:
        warnings.append(f"{row.name}: catcher fatigue risk.")
    if row.framing_score < 44:
        warnings.append(f"{row.name}: framing support below average.")

    return CatcherOutput(
        receiving_score=round(max(0, min(100, receiving)), 2),
        run_game_control_score=round(max(0, min(100, run_game)), 2),
        pitcher_support_score=round(max(0, min(100, pitcher_support)), 2),
        fatigue_adjusted_score=round(max(0, min(100, fatigue_adjusted)), 2),
        final_cam_score=round(max(0, min(100, fatigue_adjusted)), 2),
        warnings=warnings,
    )
