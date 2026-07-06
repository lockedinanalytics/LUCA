from __future__ import annotations

from luca.intelligence.mlb.bullpen.models import BullpenCollapseInput, BullpenCollapseOutput


def score_bullpen_collapse(row: BullpenCollapseInput) -> BullpenCollapseOutput:
    notes: list[str] = []

    leverage_gap = 50.0
    if row.available_high_leverage_count <= 0:
        leverage_gap += 28
        notes.append("No reliable high-leverage arms available.")
    elif row.available_high_leverage_count == 1:
        leverage_gap += 14
        notes.append("Only one high-leverage arm available.")
    else:
        leverage_gap -= min(12, row.available_high_leverage_count * 3)

    command_risk = 100 - row.command_volatility_score
    multi_run = (
        (100 - row.bullpen_quality_score) * 0.35
        + (100 - row.fatigue_score) * 0.25
        + command_risk * 0.20
        + (100 - row.inherited_runner_score) * 0.20
    )

    if row.available_total_count < 5:
        multi_run += 8
        notes.append("Overall bullpen depth is limited.")
    if row.manager_usage_score < 45:
        multi_run += 5
        notes.append("Manager usage tendency increases risk.")

    collapse = multi_run * 0.55 + leverage_gap * 0.30 + command_risk * 0.15

    return BullpenCollapseOutput(
        collapse_probability_score=round(max(0, min(100, collapse)), 2),
        multi_run_inning_risk=round(max(0, min(100, multi_run)), 2),
        command_risk=round(max(0, min(100, command_risk)), 2),
        leverage_gap_risk=round(max(0, min(100, leverage_gap)), 2),
        notes=notes,
    )
