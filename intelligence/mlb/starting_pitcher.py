from __future__ import annotations

from pydantic import BaseModel


class StartingPitcherInput(BaseModel):
    xera: float | None = None
    fip: float | None = None
    strikeout_rate: float | None = None
    walk_rate: float | None = None
    hard_hit_rate: float | None = None
    barrel_rate: float | None = None
    recent_pitch_count: int | None = None
    days_rest: int | None = None


class StartingPitcherOutput(BaseModel):
    stuff_score: float
    command_score: float
    contact_suppression_score: float
    fatigue_score: float
    final_sp_score: float
    notes: list[str]


def calculate_starting_pitcher_score(row: StartingPitcherInput) -> StartingPitcherOutput:
    notes = []

    stuff = 50.0
    if row.strikeout_rate is not None:
        stuff += (row.strikeout_rate - 22.0) * 1.1
    if row.fip is not None:
        stuff += (4.20 - row.fip) * 5

    command = 50.0
    if row.walk_rate is not None:
        command += (8.5 - row.walk_rate) * 1.4

    contact = 50.0
    if row.hard_hit_rate is not None:
        contact += (40.0 - row.hard_hit_rate) * 0.7
    if row.barrel_rate is not None:
        contact += (8.0 - row.barrel_rate) * 1.2
    if row.xera is not None:
        contact += (4.20 - row.xera) * 4

    fatigue = 60.0
    if row.recent_pitch_count is not None and row.recent_pitch_count >= 100:
        fatigue -= min(15, (row.recent_pitch_count - 95) * 0.4)
        notes.append("Recent pitch count creates fatigue watch.")
    if row.days_rest is not None:
        if row.days_rest < 4:
            fatigue -= 8
            notes.append("Short rest penalty.")
        elif row.days_rest >= 5:
            fatigue += 4

    final = stuff * 0.30 + command * 0.22 + contact * 0.28 + fatigue * 0.20
    return StartingPitcherOutput(
        stuff_score=round(max(0, min(100, stuff)), 2),
        command_score=round(max(0, min(100, command)), 2),
        contact_suppression_score=round(max(0, min(100, contact)), 2),
        fatigue_score=round(max(0, min(100, fatigue)), 2),
        final_sp_score=round(max(0, min(100, final)), 2),
        notes=notes,
    )
