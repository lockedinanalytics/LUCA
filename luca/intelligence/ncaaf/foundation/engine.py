from __future__ import annotations

from luca.intelligence.ncaaf.foundation.coaching import score_coaching_continuity
from luca.intelligence.ncaaf.foundation.models import NcaafFoundationInput, NcaafFoundationOutput
from luca.intelligence.ncaaf.foundation.roster import score_recruiting_profile, score_returning_production, score_transfer_portal


def calculate_ncaaf_foundation(row: NcaafFoundationInput) -> NcaafFoundationOutput:
    warnings: list[str] = []

    recruiting, w = score_recruiting_profile(row.recruiting); warnings.extend(w)
    returning, w = score_returning_production(row.returning_production); warnings.extend(w)
    portal, w = score_transfer_portal(row.transfer_portal); warnings.extend(w)
    coaching, w = score_coaching_continuity(row.coaching); warnings.extend(w)

    program_strength = (
        recruiting * 0.34
        + returning * 0.18
        + portal * 0.14
        + coaching * 0.16
        + row.home_field_score * 0.08
        + row.altitude_adaptation_score * 0.04
        + row.climate_adaptation_score * 0.03
        + row.travel_burden_score * 0.03
    )

    volatility = (
        max(0, 70 - returning) * 0.30
        + max(0, 65 - coaching) * 0.25
        + max(0, row.transfer_portal.portal_volatility_score - 50) * 0.35
        + max(0, 60 - row.returning_production.returning_qb_experience_score) * 0.10
    )

    final = (
        recruiting * 0.28
        + returning * 0.24
        + portal * 0.16
        + coaching * 0.20
        + program_strength * 0.12
        - volatility * 0.05
    )

    populated = 0
    total = 0
    for section in [row.recruiting, row.returning_production, row.transfer_portal, row.coaching, row]:
        data = section.model_dump()
        total += len(data)
        populated += sum(v is not None for v in data.values())
    confidence = 45 + min(45, populated / max(1, total) * 45)
    if warnings:
        confidence -= min(12, len(warnings))

    explainability = {
        "recruiting": recruiting,
        "returning_production": returning,
        "transfer_portal": portal,
        "coaching": coaching,
        "program_strength": round(program_strength, 2),
        "volatility": round(volatility, 2),
    }

    return NcaafFoundationOutput(
        roster_talent_score=recruiting,
        returning_production_score=returning,
        transfer_portal_score=portal,
        coaching_continuity_score=coaching,
        program_strength_score=round(max(0, min(100, program_strength)), 2),
        volatility_score=round(max(0, min(100, volatility)), 2),
        final_foundation_score=round(max(0, min(100, final)), 2),
        confidence=round(max(0, min(100, confidence)), 2),
        warnings=warnings,
        explainability=explainability,
    )
