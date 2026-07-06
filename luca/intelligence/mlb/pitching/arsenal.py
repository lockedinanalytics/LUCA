from __future__ import annotations

from luca.intelligence.mlb.pitching.models import PitchArsenalInput, PitchArsenalOutput


def _score_run_value(value: float | None) -> float:
    if value is None:
        return 50.0
    # Positive run value is good for hitters, bad for pitchers in many public feeds.
    return max(0, min(100, 50 - value * 2.5))


def score_pitch_arsenal(row: PitchArsenalInput) -> PitchArsenalOutput:
    notes: list[str] = []

    velocity = 50.0
    if row.fastball_velocity is not None:
        velocity += (row.fastball_velocity - 93.5) * 2.4
    if row.velocity_delta_30d is not None:
        velocity += row.velocity_delta_30d * 3.5
        if row.velocity_delta_30d <= -1.0:
            notes.append("Velocity is materially below 30-day baseline.")

    run_values = [
        _score_run_value(row.fastball_run_value),
        _score_run_value(row.slider_run_value),
        _score_run_value(row.curveball_run_value),
        _score_run_value(row.changeup_run_value),
        _score_run_value(row.cutter_run_value),
        _score_run_value(row.splitter_run_value),
    ]
    stuff = sum(run_values) / len(run_values)

    deception = 50.0
    if row.whiff_rate is not None:
        deception += (row.whiff_rate - 24.0) * 0.9
    if row.chase_rate is not None:
        deception += (row.chase_rate - 28.0) * 0.7
    if row.called_strike_rate is not None:
        deception += (row.called_strike_rate - 16.0) * 0.5

    depth = 50.0
    if row.pitch_mix_depth is not None:
        depth += (row.pitch_mix_depth - 3) * 6.0
        if row.pitch_mix_depth < 3:
            notes.append("Limited pitch mix depth increases lineup adjustment risk.")

    final = velocity * 0.25 + stuff * 0.35 + deception * 0.25 + depth * 0.15

    return PitchArsenalOutput(
        velocity_score=round(max(0, min(100, velocity)), 2),
        stuff_score=round(max(0, min(100, stuff)), 2),
        deception_score=round(max(0, min(100, deception)), 2),
        arsenal_depth_score=round(max(0, min(100, depth)), 2),
        final_arsenal_score=round(max(0, min(100, final)), 2),
        notes=notes,
    )
