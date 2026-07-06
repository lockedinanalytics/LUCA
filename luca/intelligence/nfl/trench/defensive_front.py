from __future__ import annotations

from luca.intelligence.nfl.trench.models import DefensiveFrontInput, DefensiveFrontOutput


def score_defensive_front(row: DefensiveFrontInput) -> DefensiveFrontOutput:
    warnings: list[str] = []

    pass_rush = 50.0
    if row.pressure_rate is not None:
        pass_rush += (row.pressure_rate - 34.0) * 0.85
    if row.quick_pressure_rate is not None:
        pass_rush += (row.quick_pressure_rate - 12.0) * 1.15
    if row.sack_conversion_rate is not None:
        pass_rush += (row.sack_conversion_rate - 17.0) * 0.55
    if row.pass_rush_win_rate is not None:
        pass_rush += (row.pass_rush_win_rate - 42.0) * 0.55

    run_defense = 50.0
    if row.run_stop_win_rate is not None:
        run_defense += (row.run_stop_win_rate - 31.0) * 0.85
    if row.stuff_rate is not None:
        run_defense += (row.stuff_rate - 18.0) * 0.75
    if row.missed_tackle_rate is not None:
        run_defense += (11.0 - row.missed_tackle_rate) * 0.95
    if row.gap_integrity_score is not None:
        run_defense = run_defense * 0.78 + row.gap_integrity_score * 0.22

    disruption = (
        pass_rush * 0.42
        + (row.interior_disruption_score if row.interior_disruption_score is not None else 50.0) * 0.26
        + (row.edge_containment_score if row.edge_containment_score is not None else 50.0) * 0.14
        + (row.rotation_depth_score if row.rotation_depth_score is not None else 50.0) * 0.18
        - row.fatigue_penalty
    )

    containment = (
        (row.edge_containment_score if row.edge_containment_score is not None else 50.0) * 0.45
        + (row.gap_integrity_score if row.gap_integrity_score is not None else 50.0) * 0.35
        + (100 - row.missed_tackle_rate if row.missed_tackle_rate is not None else 50.0) * 0.20
    )

    if row.pressure_rate is not None and row.pressure_rate >= 40:
        warnings.append("Defensive front generates elevated pressure.")
    if row.missed_tackle_rate is not None and row.missed_tackle_rate >= 14:
        warnings.append("Missed tackle rate weakens front reliability.")
    if row.fatigue_penalty >= 8:
        warnings.append("Defensive front fatigue penalty is material.")

    final = pass_rush * 0.34 + run_defense * 0.28 + disruption * 0.24 + containment * 0.14

    return DefensiveFrontOutput(
        pass_rush_score=round(max(0, min(100, pass_rush)), 2),
        run_defense_score=round(max(0, min(100, run_defense)), 2),
        disruption_score=round(max(0, min(100, disruption)), 2),
        containment_score=round(max(0, min(100, containment)), 2),
        final_front_score=round(max(0, min(100, final)), 2),
        warnings=warnings,
    )
