from __future__ import annotations

from luca.intelligence.nfl.quarterback.models import NflQuarterbackEfficiencyInput


def score_qb_efficiency(row: NflQuarterbackEfficiencyInput) -> tuple[float, list[str]]:
    warnings: list[str] = []
    score = 50.0

    if row.epa_per_play is not None:
        score += row.epa_per_play * 115
    if row.success_rate is not None:
        score += (row.success_rate - 45.0) * 0.70
    if row.cpoe is not None:
        score += row.cpoe * 0.95
    if row.anya is not None:
        score += (row.anya - 6.3) * 3.8
    if row.third_down_success_rate is not None:
        score += (row.third_down_success_rate - 40.0) * 0.35
    if row.red_zone_efficiency is not None:
        score += (row.red_zone_efficiency - 55.0) * 0.25

    if row.epa_per_play is not None and row.epa_per_play < -0.05:
        warnings.append("QB efficiency below replacement-level threshold.")
    if row.cpoe is not None and row.cpoe < -3:
        warnings.append("Completion efficiency materially below expectation.")

    return round(max(0, min(100, score)), 2), warnings
