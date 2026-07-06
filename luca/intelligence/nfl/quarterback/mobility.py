from __future__ import annotations

from luca.intelligence.nfl.quarterback.models import NflQuarterbackMobilityInput


def score_qb_mobility(row: NflQuarterbackMobilityInput) -> tuple[float, list[str]]:
    warnings: list[str] = []
    score = 50.0

    if row.scramble_epa is not None:
        score += row.scramble_epa * 40
    if row.designed_run_epa is not None:
        score += row.designed_run_epa * 32
    if row.pressure_escape_score is not None:
        score = score * 0.70 + row.pressure_escape_score * 0.30
    if row.rushing_success_rate is not None:
        score += (row.rushing_success_rate - 42.0) * 0.32

    if row.pressure_escape_score is not None and row.pressure_escape_score >= 62:
        warnings.append("Mobility materially raises floor against pressure.")
    if row.scramble_epa is not None and row.scramble_epa < -0.10:
        warnings.append("Scramble value is inefficient.")

    return round(max(0, min(100, score)), 2), warnings
