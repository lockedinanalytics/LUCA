from __future__ import annotations

from luca.intelligence.mlb.pitching.models import FatigueInput, FatigueOutput


def score_pitcher_fatigue(row: FatigueInput) -> FatigueOutput:
    notes: list[str] = []

    workload = 70.0
    if row.pitches_last_start is not None:
        if row.pitches_last_start > 100:
            workload -= min(18, (row.pitches_last_start - 100) * 0.6)
            notes.append("High pitch count last start.")
        elif row.pitches_last_start < 80:
            workload += 3
    if row.pitches_last_7_days is not None:
        workload -= min(16, max(0, row.pitches_last_7_days - 105) * 0.20)
    if row.pitches_last_30_days is not None:
        workload -= min(14, max(0, row.pitches_last_30_days - 440) * 0.035)

    recovery = 60.0
    if row.days_rest is not None:
        if row.days_rest < 4:
            recovery -= 12
            notes.append("Short-rest start.")
        elif row.days_rest == 4:
            recovery += 0
        elif row.days_rest >= 5:
            recovery += 6

    stability = 60.0
    if row.velocity_delta_30d is not None:
        stability += row.velocity_delta_30d * 4
        if row.velocity_delta_30d <= -1:
            notes.append("Velocity decline supports fatigue signal.")
    if row.spin_delta_30d is not None:
        stability += row.spin_delta_30d * 0.04
    if row.release_drift_score is not None:
        stability = stability * 0.70 + row.release_drift_score * 0.30

    final = workload * 0.35 + recovery * 0.35 + stability * 0.30

    return FatigueOutput(
        workload_score=round(max(0, min(100, workload)), 2),
        recovery_score=round(max(0, min(100, recovery)), 2),
        signal_stability_score=round(max(0, min(100, stability)), 2),
        final_fatigue_score=round(max(0, min(100, final)), 2),
        notes=notes,
    )
