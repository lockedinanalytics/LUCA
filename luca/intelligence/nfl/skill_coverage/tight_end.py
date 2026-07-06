from __future__ import annotations

from luca.intelligence.nfl.skill_coverage.models import TightEndInput, TightEndOutput


def score_tight_end(row: TightEndInput) -> TightEndOutput:
    warnings: list[str] = []

    receiving = (
        (row.route_rate_score if row.route_rate_score is not None else 50.0) * 0.28
        + (row.yards_per_route_score if row.yards_per_route_score is not None else 50.0) * 0.32
        + (row.linebacker_matchup_score if row.linebacker_matchup_score is not None else 50.0) * 0.20
        + (row.safety_matchup_score if row.safety_matchup_score is not None else 50.0) * 0.20
    )
    red_zone = (
        (row.red_zone_usage_score if row.red_zone_usage_score is not None else 50.0) * 0.55
        + receiving * 0.30
        + (row.blocking_support_score if row.blocking_support_score is not None else 50.0) * 0.15
    )
    flex = (
        receiving * 0.40
        + (row.blocking_support_score if row.blocking_support_score is not None else 50.0) * 0.30
        + red_zone * 0.30
    )

    if row.red_zone_usage_score is not None and row.red_zone_usage_score >= 62:
        warnings.append("Tight end materially improves red-zone pass structure.")
    if row.blocking_support_score is not None and row.blocking_support_score < 42:
        warnings.append("Tight end blocking support is weak.")

    final = receiving * 0.42 + red_zone * 0.30 + flex * 0.28

    return TightEndOutput(
        receiving_matchup_score=round(max(0, min(100, receiving)), 2),
        red_zone_score=round(max(0, min(100, red_zone)), 2),
        formation_flex_score=round(max(0, min(100, flex)), 2),
        final_te_score=round(max(0, min(100, final)), 2),
        warnings=warnings,
    )
