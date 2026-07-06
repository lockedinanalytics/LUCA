from __future__ import annotations

from luca.intelligence.mlb.bullpen.models import RelieverAvailabilityOutput, RelieverUsageInput


HIGH_LEVERAGE_ROLES = {"closer", "setup", "fireman", "primary_lefty"}


def score_reliever_availability(row: RelieverUsageInput) -> RelieverAvailabilityOutput:
    warnings: list[str] = []

    availability = 76.0
    fatigue = 76.0

    fatigue -= min(24, row.pitches_yesterday * 0.45)
    fatigue -= min(20, row.pitches_last_3_days * 0.18)
    fatigue -= row.appearances_last_3_days * 3.0

    if row.back_to_back:
        fatigue -= 10
        warnings.append("Back-to-back usage.")
    if row.three_in_four:
        fatigue -= 14
        warnings.append("Three-in-four usage.")

    if row.available_override is False:
        availability = 0
        fatigue = 0
        warnings.append("Availability override: unavailable.")
    elif row.available_override is True:
        availability += 8

    quality = row.season_quality_score * 0.45 + row.recent_quality_score * 0.35 + row.inherited_runner_score * 0.20
    leverage = row.leverage_role_score * 0.60 + quality * 0.25 + fatigue * 0.15

    usable = availability >= 35 and fatigue >= 32
    if not usable:
        warnings.append("Reliever usage risk exceeds availability threshold.")

    return RelieverAvailabilityOutput(
        name=row.name,
        role=row.role,
        availability_score=round(max(0, min(100, availability)), 2),
        fatigue_score=round(max(0, min(100, fatigue)), 2),
        quality_score=round(max(0, min(100, quality)), 2),
        leverage_score=round(max(0, min(100, leverage)), 2),
        usable=usable,
        warnings=warnings,
    )


def score_all_relievers(relievers: list[RelieverUsageInput]) -> list[RelieverAvailabilityOutput]:
    return [score_reliever_availability(row) for row in relievers]
