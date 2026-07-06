from __future__ import annotations

from fastapi import APIRouter

from luca.intelligence.mlb.bullpen.availability import score_reliever_availability
from luca.intelligence.mlb.bullpen.collapse import score_bullpen_collapse
from luca.intelligence.mlb.bullpen.engine import calculate_bullpen_intelligence
from luca.intelligence.mlb.bullpen.hierarchy import score_bullpen_hierarchy
from luca.intelligence.mlb.bullpen.models import (
    BullpenCollapseInput,
    BullpenHierarchyInput,
    BullpenIntelligenceInput,
    RelieverUsageInput,
)

router = APIRouter(prefix="/intelligence/mlb/bullpen", tags=["mlb-bullpen"])


def sample_relievers() -> list[RelieverUsageInput]:
    return [
        RelieverUsageInput(name="Closer A", role="closer", pitches_yesterday=18, pitches_last_3_days=42, appearances_last_3_days=2, leverage_role_score=82, season_quality_score=76, recent_quality_score=74, inherited_runner_score=70, command_volatility_score=68),
        RelieverUsageInput(name="Setup B", role="setup", pitches_yesterday=0, pitches_last_3_days=24, appearances_last_3_days=1, leverage_role_score=76, season_quality_score=70, recent_quality_score=72, inherited_runner_score=66, command_volatility_score=64),
        RelieverUsageInput(name="Lefty C", role="primary_lefty", pitches_yesterday=12, pitches_last_3_days=28, appearances_last_3_days=2, leverage_role_score=68, season_quality_score=64, recent_quality_score=60, inherited_runner_score=62, command_volatility_score=58),
        RelieverUsageInput(name="Long D", role="long", pitches_yesterday=0, pitches_last_3_days=15, appearances_last_3_days=1, leverage_role_score=50, season_quality_score=58, recent_quality_score=56, inherited_runner_score=55, command_volatility_score=60),
    ]


@router.get("/reliever/sample")
async def reliever_sample():
    return score_reliever_availability(sample_relievers()[0]).model_dump()


@router.get("/hierarchy/sample")
async def hierarchy_sample():
    return score_bullpen_hierarchy(BullpenHierarchyInput(relievers=sample_relievers())).model_dump()


@router.get("/collapse/sample")
async def collapse_sample():
    return score_bullpen_collapse(BullpenCollapseInput(
        available_total_count=4,
        available_high_leverage_count=2,
        bullpen_quality_score=66,
        fatigue_score=62,
        command_volatility_score=60,
        inherited_runner_score=64,
        manager_usage_score=55,
    )).model_dump()


@router.get("/bsi-v2/sample")
async def bsi_v2_sample():
    return calculate_bullpen_intelligence(BullpenIntelligenceInput(relievers=sample_relievers(), manager_usage_score=55, game_leverage_projection=65)).model_dump()
