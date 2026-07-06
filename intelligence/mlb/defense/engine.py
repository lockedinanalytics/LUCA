from __future__ import annotations

from luca.intelligence.mlb.defense.baserunning import score_baserunner_prevention
from luca.intelligence.mlb.defense.catcher import score_catcher
from luca.intelligence.mlb.defense.fielding import score_fielding_unit
from luca.intelligence.mlb.defense.models import DefensiveIntelligenceInput, DefensiveIntelligenceOutput


def calculate_defensive_intelligence(row: DefensiveIntelligenceInput) -> DefensiveIntelligenceOutput:
    catcher = score_catcher(row.catcher)
    fielding = score_fielding_unit(row.fielding)
    baserunner = score_baserunner_prevention(row.baserunner_prevention)

    warnings = []
    warnings.extend(catcher.warnings)
    warnings.extend(fielding.warnings)
    warnings.extend(baserunner.warnings)

    contact_support = (
        fielding.final_fielding_score * 0.45
        + catcher.pitcher_support_score * 0.25
        + row.pitcher_contact_profile_score * 0.20
        + row.park_defensive_difficulty_score * 0.10
    )

    defensive_run_prevention = (
        catcher.final_cam_score * 0.28
        + fielding.final_fielding_score * 0.34
        + baserunner.pressure_adjusted_score * 0.16
        + contact_support * 0.22
    )

    populated_sections = 3
    confidence = 55 + populated_sections * 10
    if warnings:
        confidence -= min(15, len(warnings) * 2)

    explainability = {
        "cam": catcher.final_cam_score,
        "fielding": fielding.final_fielding_score,
        "baserunner_prevention": baserunner.pressure_adjusted_score,
        "contact_support": round(contact_support, 2),
    }

    return DefensiveIntelligenceOutput(
        cam_score=catcher.final_cam_score,
        fielding_score=fielding.final_fielding_score,
        baserunner_prevention_score=baserunner.pressure_adjusted_score,
        contact_support_score=round(max(0, min(100, contact_support)), 2),
        defensive_run_prevention_score=round(max(0, min(100, defensive_run_prevention)), 2),
        confidence=round(max(0, min(100, confidence)), 2),
        warnings=warnings,
        explainability=explainability,
    )
