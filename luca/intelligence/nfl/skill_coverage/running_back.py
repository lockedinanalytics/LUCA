from __future__ import annotations

from luca.intelligence.nfl.skill_coverage.models import RunningBackInput, RunningBackOutput


def score_running_back(row: RunningBackInput) -> RunningBackOutput:
    warnings: list[str] = []

    rushing = (
        (row.rushing_efficiency_score if row.rushing_efficiency_score is not None else 50.0) * 0.32
        + (row.explosive_run_score if row.explosive_run_score is not None else 50.0) * 0.22
        + (row.yards_after_contact_score if row.yards_after_contact_score is not None else 50.0) * 0.22
        + (row.vision_score if row.vision_score is not None else 50.0) * 0.24
    )
    receiving = row.receiving_utilization_score if row.receiving_utilization_score is not None else 50.0
    protection = row.pass_protection_score if row.pass_protection_score is not None else 50.0
    goal_line = (
        (row.goal_line_usage_score if row.goal_line_usage_score is not None else 50.0) * 0.55
        + rushing * 0.35
        + protection * 0.10
    )

    if receiving >= 60:
        warnings.append("RB receiving utility improves pass-game flexibility.")
    if protection < 42:
        warnings.append("RB pass protection is a pressure vulnerability.")

    final = rushing * 0.42 + receiving * 0.20 + protection * 0.16 + goal_line * 0.22

    return RunningBackOutput(
        rushing_value_score=round(max(0, min(100, rushing)), 2),
        receiving_value_score=round(max(0, min(100, receiving)), 2),
        protection_value_score=round(max(0, min(100, protection)), 2),
        goal_line_value_score=round(max(0, min(100, goal_line)), 2),
        final_rb_score=round(max(0, min(100, final)), 2),
        warnings=warnings,
    )
