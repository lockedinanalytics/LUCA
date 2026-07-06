from __future__ import annotations

from luca.intelligence.nfl.quarterback.models import NflQuarterbackPressureInput


def score_qb_pressure(row: NflQuarterbackPressureInput) -> tuple[float, list[str]]:
    warnings: list[str] = []
    score = 50.0

    if row.pressure_epa_per_play is not None:
        score += row.pressure_epa_per_play * 85
    if row.pressure_to_sack_rate is not None:
        score += (18.0 - row.pressure_to_sack_rate) * 0.9
    if row.blitz_epa_per_play is not None:
        score += row.blitz_epa_per_play * 70
    if row.clean_pocket_epa_per_play is not None:
        score += row.clean_pocket_epa_per_play * 35
    if row.time_to_throw is not None:
        if row.time_to_throw > 3.0:
            score -= (row.time_to_throw - 3.0) * 4.5
        elif row.time_to_throw < 2.45:
            score += (2.45 - row.time_to_throw) * 2.0

    if row.pressure_to_sack_rate is not None and row.pressure_to_sack_rate > 24:
        warnings.append("Pressure-to-sack rate is a material drive-killer.")
    if row.pressure_epa_per_play is not None and row.pressure_epa_per_play < -0.35:
        warnings.append("QB collapses materially under pressure.")

    return round(max(0, min(100, score)), 2), warnings
