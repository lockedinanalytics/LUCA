from __future__ import annotations

from luca.intelligence.nfl.quarterback.models import NflQuarterbackMatchupInput


def score_qb_matchup(row: NflQuarterbackMatchupInput) -> tuple[float, list[str]]:
    warnings: list[str] = []

    pressure_component = 100 - row.opponent_pressure_score
    coverage_component = 100 - row.opponent_coverage_score
    blitz_component = 100 - row.opponent_blitz_rate_score

    score = (
        pressure_component * 0.20
        + coverage_component * 0.22
        + blitz_component * 0.12
        + row.offensive_line_support_score * 0.18
        + row.receiver_separation_score * 0.16
        + row.coaching_pass_design_score * 0.12
    )

    if row.opponent_pressure_score >= 62 and row.offensive_line_support_score < 50:
        warnings.append("Opponent pressure versus OL support is a mismatch risk.")
    if row.opponent_coverage_score >= 62 and row.receiver_separation_score < 50:
        warnings.append("Coverage versus separation profile is unfavorable.")

    return round(max(0, min(100, score)), 2), warnings
