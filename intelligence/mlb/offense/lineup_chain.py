from __future__ import annotations

from statistics import mean

from luca.intelligence.mlb.offense.hitter import score_hitter
from luca.intelligence.mlb.offense.models import LineupChainInput, LineupChainOutput


def score_lineup_chain(row: LineupChainInput) -> LineupChainOutput:
    warnings: list[str] = []

    if not row.hitters:
        return LineupChainOutput(
            top_four_score=50.0,
            bottom_five_score=50.0,
            on_base_chain_score=50.0,
            power_cascade_score=50.0,
            strikeout_cluster_risk=50.0,
            lineup_depth_score=50.0,
            bench_adjustment_score=50.0,
            final_chain_score=50.0,
            warnings=["No hitter-level lineup data supplied."],
            hitter_scores={},
        )

    scored = [score_hitter(h) for h in row.hitters]
    scored_by_spot = sorted(scored, key=lambda h: h.lineup_spot)

    for h in scored:
        warnings.extend(h.warnings)

    top = [h.final_hitter_score for h in scored_by_spot if h.lineup_spot <= 4]
    bottom = [h.final_hitter_score for h in scored_by_spot if h.lineup_spot >= 5]

    top_four = mean(top) if top else 50.0
    bottom_five = mean(bottom) if bottom else 50.0

    # Chain score rewards consecutive strong hitters.
    chain_segments = []
    for left, right in zip(scored_by_spot, scored_by_spot[1:]):
        chain_segments.append((left.on_base_score * 0.50 + right.damage_score * 0.50))
    on_base_chain = mean(chain_segments) if chain_segments else 50.0

    power_segments = []
    for trio_start in range(max(0, len(scored_by_spot) - 2)):
        trio = scored_by_spot[trio_start:trio_start + 3]
        power_segments.append(mean([h.damage_score for h in trio]))
    power_cascade = max(power_segments) if power_segments else 50.0

    # Higher value means more risk.
    low_disciplined_clusters = []
    for trio_start in range(max(0, len(scored_by_spot) - 2)):
        trio = scored_by_spot[trio_start:trio_start + 3]
        low_disciplined_clusters.append(100 - mean([h.discipline_score for h in trio]))
    strikeout_cluster_risk = max(low_disciplined_clusters) if low_disciplined_clusters else 50.0

    depth = top_four * 0.45 + bottom_five * 0.45 + row.bench_score * 0.10
    bench = row.bench_score * 0.55 + row.pinch_hit_score * 0.45

    if len(row.hitters) < 9:
        depth -= (9 - len(row.hitters)) * 3.0
        warnings.append("Incomplete lineup supplied.")
    if strikeout_cluster_risk >= 62:
        warnings.append("Strikeout cluster risk detected.")

    final = (
        top_four * 0.24
        + bottom_five * 0.18
        + on_base_chain * 0.22
        + power_cascade * 0.18
        + depth * 0.12
        + bench * 0.06
        - max(0, strikeout_cluster_risk - 50) * 0.12
    )

    return LineupChainOutput(
        top_four_score=round(max(0, min(100, top_four)), 2),
        bottom_five_score=round(max(0, min(100, bottom_five)), 2),
        on_base_chain_score=round(max(0, min(100, on_base_chain)), 2),
        power_cascade_score=round(max(0, min(100, power_cascade)), 2),
        strikeout_cluster_risk=round(max(0, min(100, strikeout_cluster_risk)), 2),
        lineup_depth_score=round(max(0, min(100, depth)), 2),
        bench_adjustment_score=round(max(0, min(100, bench)), 2),
        final_chain_score=round(max(0, min(100, final)), 2),
        warnings=warnings,
        hitter_scores={h.name: h.final_hitter_score for h in scored},
    )
