from __future__ import annotations

from fastapi import APIRouter

from luca.intelligence.ncaaf.foundation.engine import calculate_ncaaf_foundation
from luca.intelligence.ncaaf.foundation.models import (
    CoachingContinuityInput,
    NcaafFoundationInput,
    RecruitingProfileInput,
    ReturningProductionInput,
    TransferPortalInput,
)
from luca.providers.ncaaf.registry import sample_registry
from luca.providers.ncaaf.schedule import StaticNcaafScheduleProvider

router = APIRouter(prefix="/intelligence/ncaaf/foundation", tags=["ncaaf-foundation"])


@router.get("/registry/sample")
async def registry_sample():
    return [row.model_dump() for row in sample_registry()]


@router.get("/schedule/sample")
async def schedule_sample(season: int = 2026, week: int = 1):
    return [row.model_dump() for row in StaticNcaafScheduleProvider().get_games(season, week)]


@router.get("/foundation/sample")
async def foundation_sample():
    return calculate_ncaaf_foundation(NcaafFoundationInput(
        recruiting=RecruitingProfileInput(recruiting_composite_score=72, blue_chip_ratio=0.58, avg_star_rating=3.9, recruiting_momentum_score=66, position_group_depth_score=68),
        returning_production=ReturningProductionInput(offensive_returning_production_pct=68, defensive_returning_production_pct=61, returning_starters_offense=8, returning_starters_defense=7, returning_qb_experience_score=64, offensive_line_continuity_score=62),
        transfer_portal=TransferPortalInput(transfer_gain_score=60, transfer_loss_score=42, quarterback_transfer_score=58, defensive_transfer_score=56, portal_volatility_score=48),
        coaching=CoachingContinuityInput(head_coach_continuity_score=72, offensive_coordinator_continuity_score=65, defensive_coordinator_continuity_score=66, scheme_stability_score=70, staff_turnover_penalty=2, historical_system_performance_score=68),
        home_field_score=66,
        travel_burden_score=58,
        altitude_adaptation_score=54,
        climate_adaptation_score=56,
    )).model_dump()
