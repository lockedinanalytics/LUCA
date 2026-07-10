from __future__ import annotations

from statistics import mean

from luca.intelligence.mlb.offense.hitter import score_hitter
from luca.intelligence.mlb.offense.models import (
    LineupChainInput,
    LineupChainOutput,
)


LINEUP_CHAIN_ENGINE_VERSION = "lineup_chain_governance_diagnostic_cleanup"


def _clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, float(value)))


def score_lineup_chain(row: LineupChainInput) -> LineupChainOutput:
    """
    Score lineup sequencing, depth, on-base chaining, power cascading,
    strikeout clustering, and bench contribution.

    Governance migration note:
    Lineup Chain is an upstream offensive intelligence component only. It does
    not select plays, certify Presidential eligibility, rank wagers, apply
    Governance penalties, or assign units.
    """
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
            warnings=[
                "No hitter-level lineup data supplied.",
                "Lineup Chain remains diagnostic only; Governance Score is the certification authority.",
            ],
            hitter_scores={},
        )

    scored = [score_hitter(h) for h in row.hitters]
    scored_by_spot = sorted(scored, key=lambda h: h.lineup_spot)

    for hitter in scored:
        warnings.extend(hitter.warnings)

    top = [
        hitter.final_hitter_score
        for hitter in scored_by_spot
        if hitter.lineup_spot <= 4
    ]
    bottom = [
        hitter.final_hitter_score
        for hitter in scored_by_spot
        if hitter.lineup_spot >= 5
    ]

    top_four = mean(top) if top else 50.0
    bottom_five = mean(bottom) if bottom else 50.0

    chain_segments = [
        left.on_base_score * 0.50 + right.damage_score * 0.50
        for left, right in zip(scored_by_spot, scored_by_spot[1:])
    ]
    on_base_chain = mean(chain_segments) if chain_segments else 50.0

    power_segments = []
    for trio_start in range(max(0, len(scored_by_spot) - 2)):
        trio = scored_by_spot[trio_start : trio_start + 3]
        power_segments.append(mean([hitter.damage_score for hitter in trio]))
    power_cascade = max(power_segments) if power_segments else 50.0

    low_discipline_clusters = []
    for trio_start in range(max(0, len(scored_by_spot) - 2)):
        trio = scored_by_spot[trio_start : trio_start + 3]
        low_discipline_clusters.append(
            100.0 - mean([hitter.discipline_score for hitter in trio])
        )
    strikeout_cluster_risk = (
        max(low_discipline_clusters)
        if low_discipline_clusters
        else 50.0
    )

    depth = top_four * 0.45 + bottom_five * 0.45 + row.bench_score * 0.10
    bench = row.bench_score * 0.55 + row.pinch_hit_score * 0.45

    if len(row.hitters) < 9:
        depth -= (9 - len(row.hitters)) * 3.0
        warnings.append(
            f"Incomplete lineup supplied: {len(row.hitters)}/9 hitters."
        )

    if strikeout_cluster_risk >= 62.0:
        warnings.append("Strikeout cluster risk detected.")

    final = (
        top_four * 0.24
        + bottom_five * 0.18
        + on_base_chain * 0.22
        + power_cascade * 0.18
        + depth * 0.12
        + bench * 0.06
        - max(0.0, strikeout_cluster_risk - 50.0) * 0.12
    )

    final = _clamp(final)

    warnings.append(
        "Lineup Chain is diagnostic only; Governance Score remains the single certification authority."
    )

    return LineupChainOutput(
        top_four_score=round(_clamp(top_four), 2),
        bottom_five_score=round(_clamp(bottom_five), 2),
        on_base_chain_score=round(_clamp(on_base_chain), 2),
        power_cascade_score=round(_clamp(power_cascade), 2),
        strikeout_cluster_risk=round(_clamp(strikeout_cluster_risk), 2),
        lineup_depth_score=round(_clamp(depth), 2),
        bench_adjustment_score=round(_clamp(bench), 2),
        final_chain_score=round(final, 2),
        warnings=warnings,
        hitter_scores={
            hitter.name: round(_clamp(hitter.final_hitter_score), 2)
            for hitter in scored
        },
    )
