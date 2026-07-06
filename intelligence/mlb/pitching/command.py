from __future__ import annotations

from luca.intelligence.mlb.pitching.models import CommandInput, CommandOutput


def score_command(row: CommandInput) -> CommandOutput:
    notes: list[str] = []

    zone_control = 50.0
    if row.strike_rate is not None:
        zone_control += (row.strike_rate - 64.0) * 0.9
    if row.zone_rate is not None:
        zone_control += (row.zone_rate - 42.0) * 0.6
    if row.walk_rate is not None:
        zone_control += (8.2 - row.walk_rate) * 1.6

    count_leverage = 50.0
    if row.first_pitch_strike_rate is not None:
        count_leverage += (row.first_pitch_strike_rate - 61.0) * 0.9
        if row.first_pitch_strike_rate < 57:
            notes.append("Below-average first-pitch strike rate creates count leverage risk.")

    mistake = 50.0
    if row.edge_rate is not None:
        mistake += (row.edge_rate - 41.0) * 0.8
    if row.heart_rate is not None:
        mistake += (24.0 - row.heart_rate) * 1.1
        if row.heart_rate > 28:
            notes.append("Elevated heart-zone rate increases damage risk.")
    if row.release_consistency_score is not None:
        mistake = mistake * 0.75 + row.release_consistency_score * 0.25

    final = zone_control * 0.40 + count_leverage * 0.25 + mistake * 0.35

    return CommandOutput(
        zone_control_score=round(max(0, min(100, zone_control)), 2),
        count_leverage_score=round(max(0, min(100, count_leverage)), 2),
        mistake_avoidance_score=round(max(0, min(100, mistake)), 2),
        final_command_score=round(max(0, min(100, final)), 2),
        notes=notes,
    )
