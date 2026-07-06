from __future__ import annotations

from statistics import mean

from luca.intelligence.mlb.bullpen.availability import score_all_relievers
from luca.intelligence.mlb.bullpen.models import BullpenHierarchyInput, BullpenHierarchyOutput


def _role_score(rows, roles: set[str]) -> float:
    role_rows = [r for r in rows if r.role in roles and r.usable]
    if not role_rows:
        return 35.0
    return mean([r.leverage_score for r in role_rows])


def score_bullpen_hierarchy(row: BullpenHierarchyInput) -> BullpenHierarchyOutput:
    relievers = score_all_relievers(row.relievers)
    warnings: list[str] = []

    closer = _role_score(relievers, {"closer"})
    setup = _role_score(relievers, {"setup", "fireman"})
    lefty = _role_score(relievers, {"primary_lefty", "lefty"})
    long_relief = _role_score(relievers, {"long", "bulk", "middle"})

    usable = [r for r in relievers if r.usable]
    high_lev = [r for r in usable if r.role in {"closer", "setup", "fireman", "primary_lefty"}]

    if closer <= 40:
        warnings.append("Closer slot is unavailable or weak.")
    if len(high_lev) < 2:
        warnings.append("High-leverage depth is thin.")

    depth = mean([r.quality_score for r in usable]) if usable else 30.0

    return BullpenHierarchyOutput(
        closer_score=round(max(0, min(100, closer)), 2),
        setup_score=round(max(0, min(100, setup)), 2),
        lefty_score=round(max(0, min(100, lefty)), 2),
        long_relief_score=round(max(0, min(100, long_relief)), 2),
        depth_score=round(max(0, min(100, depth)), 2),
        available_high_leverage_count=len(high_lev),
        available_total_count=len(usable),
        warnings=warnings,
    )
