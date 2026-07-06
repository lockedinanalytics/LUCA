from __future__ import annotations

from statistics import mean

from luca.intelligence.mlb.bullpen.availability import score_all_relievers
from luca.intelligence.mlb.bullpen.collapse import score_bullpen_collapse
from luca.intelligence.mlb.bullpen.hierarchy import score_bullpen_hierarchy
from luca.intelligence.mlb.bullpen.models import (
    BullpenCollapseInput,
    BullpenHierarchyInput,
    BullpenIntelligenceInput,
    BullpenIntelligenceOutput,
)


def calculate_bullpen_intelligence(row: BullpenIntelligenceInput) -> BullpenIntelligenceOutput:
    warnings: list[str] = []

    if not row.relievers:
        return BullpenIntelligenceOutput(
            availability_score=50.0,
            fatigue_score=50.0,
            quality_score=50.0,
            leverage_score=50.0,
            hierarchy_score=50.0,
            collapse_risk_score=50.0,
            final_bsi=50.0,
            confidence=35.0,
            warnings=["No reliever-level bullpen data supplied."],
            explainability={},
        )

    relievers = score_all_relievers(row.relievers)
    hierarchy = score_bullpen_hierarchy(BullpenHierarchyInput(relievers=row.relievers))

    usable = [r for r in relievers if r.usable]
    base_rows = usable if usable else relievers

    availability = mean([r.availability_score for r in base_rows])
    fatigue = mean([r.fatigue_score for r in base_rows])
    quality = mean([r.quality_score for r in base_rows])
    leverage = mean([r.leverage_score for r in base_rows])
    inherited = mean([r.inherited_runner_score for r in row.relievers])
    command = mean([r.command_volatility_score for r in row.relievers])

    hierarchy_score = (
        hierarchy.closer_score * 0.25
        + hierarchy.setup_score * 0.25
        + hierarchy.lefty_score * 0.15
        + hierarchy.long_relief_score * 0.10
        + hierarchy.depth_score * 0.25
    )

    collapse = score_bullpen_collapse(BullpenCollapseInput(
        available_total_count=hierarchy.available_total_count,
        available_high_leverage_count=hierarchy.available_high_leverage_count,
        bullpen_quality_score=quality,
        fatigue_score=fatigue,
        command_volatility_score=command,
        inherited_runner_score=inherited,
        manager_usage_score=row.manager_usage_score,
    ))

    warnings.extend(hierarchy.warnings)
    for reliever in relievers:
        warnings.extend([f"{reliever.name}: {warning}" for warning in reliever.warnings])
    warnings.extend(collapse.notes)

    # BSI is a positive score: higher means healthier/better bullpen state.
    final = (
        availability * 0.22
        + fatigue * 0.22
        + quality * 0.18
        + leverage * 0.16
        + hierarchy_score * 0.14
        + (100 - collapse.collapse_probability_score) * 0.08
    )

    populated = len(row.relievers)
    confidence = min(95, 45 + populated * 6)

    explainability = {
        "availability": round(availability, 2),
        "fatigue": round(fatigue, 2),
        "quality": round(quality, 2),
        "leverage": round(leverage, 2),
        "hierarchy": round(hierarchy_score, 2),
        "collapse_risk": collapse.collapse_probability_score,
    }

    return BullpenIntelligenceOutput(
        availability_score=round(max(0, min(100, availability)), 2),
        fatigue_score=round(max(0, min(100, fatigue)), 2),
        quality_score=round(max(0, min(100, quality)), 2),
        leverage_score=round(max(0, min(100, leverage)), 2),
        hierarchy_score=round(max(0, min(100, hierarchy_score)), 2),
        collapse_risk_score=collapse.collapse_probability_score,
        final_bsi=round(max(0, min(100, final)), 2),
        confidence=round(confidence, 2),
        warnings=warnings,
        explainability=explainability,
    )
