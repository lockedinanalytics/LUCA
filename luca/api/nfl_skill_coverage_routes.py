from __future__ import annotations

from fastapi import APIRouter

from luca.intelligence.nfl.skill_coverage.coverage import score_coverage_unit
from luca.intelligence.nfl.skill_coverage.matchup import calculate_skill_coverage_matchup
from luca.intelligence.nfl.skill_coverage.models import CoverageUnitInput, ReceiverUnitInput, RunningBackInput, SkillCoverageMatchupInput, TightEndInput
from luca.intelligence.nfl.skill_coverage.receivers import score_receiver_unit
from luca.intelligence.nfl.skill_coverage.running_back import score_running_back
from luca.intelligence.nfl.skill_coverage.tight_end import score_tight_end

router = APIRouter(prefix="/intelligence/nfl/skill-coverage", tags=["nfl-skill-coverage"])


@router.get("/receivers/sample")
async def receivers_sample():
    return score_receiver_unit(ReceiverUnitInput(
        separation_score=61, target_share_score=59, route_participation_score=62,
        explosive_route_score=60, contested_catch_score=56, yards_after_catch_score=58,
        slot_efficiency_score=57, boundary_efficiency_score=59, depth_score=56,
    )).model_dump()


@router.get("/coverage/sample")
async def coverage_sample():
    return score_coverage_unit(CoverageUnitInput(
        man_coverage_score=56, zone_coverage_score=58, pressure_coverage_synergy_score=57,
        explosive_pass_prevention_score=55, slot_coverage_score=54, boundary_coverage_score=57,
        safety_help_score=58, linebacker_coverage_score=52, communication_score=59,
    )).model_dump()


@router.get("/matchup/sample")
async def matchup_sample():
    return calculate_skill_coverage_matchup(SkillCoverageMatchupInput(
        receivers=ReceiverUnitInput(separation_score=61, target_share_score=59, route_participation_score=62, explosive_route_score=60, contested_catch_score=56, yards_after_catch_score=58, slot_efficiency_score=57, boundary_efficiency_score=59, depth_score=56),
        tight_end=TightEndInput(route_rate_score=55, yards_per_route_score=56, red_zone_usage_score=60, blocking_support_score=54, linebacker_matchup_score=57, safety_matchup_score=55),
        running_back=RunningBackInput(rushing_efficiency_score=56, receiving_utilization_score=58, pass_protection_score=55, explosive_run_score=57, yards_after_contact_score=56, vision_score=58, goal_line_usage_score=59),
        coverage=CoverageUnitInput(man_coverage_score=56, zone_coverage_score=58, pressure_coverage_synergy_score=57, explosive_pass_prevention_score=55, slot_coverage_score=54, boundary_coverage_score=57, safety_help_score=58, linebacker_coverage_score=52, communication_score=59),
        quarterback_accuracy_score=61,
        pass_protection_score=58,
        offensive_scheme_score=59,
        defensive_scheme_score=55,
    )).model_dump()
