from __future__ import annotations

from fastapi import APIRouter

from luca.intelligence.mlb.pitching.models import (
    CommandInput,
    ContactManagementInput,
    FatigueInput,
    MatchupInput,
    PitchArsenalInput,
    StartingPitcherIntelligenceInput,
)
from luca.intelligence.mlb.pitching.arsenal import score_pitch_arsenal
from luca.intelligence.mlb.pitching.command import score_command
from luca.intelligence.mlb.pitching.contact import score_contact_management
from luca.intelligence.mlb.pitching.engine import calculate_starting_pitcher_intelligence
from luca.intelligence.mlb.pitching.fatigue import score_pitcher_fatigue
from luca.intelligence.mlb.pitching.matchup import score_pitcher_matchup

router = APIRouter(prefix="/intelligence/mlb/pitching", tags=["mlb-pitching"])


@router.get("/arsenal/sample")
async def arsenal_sample():
    return score_pitch_arsenal(PitchArsenalInput(
        fastball_velocity=95.2,
        velocity_delta_30d=0.4,
        fastball_run_value=-3,
        slider_run_value=-5,
        curveball_run_value=1,
        changeup_run_value=-2,
        whiff_rate=29,
        chase_rate=32,
        called_strike_rate=18,
        pitch_mix_depth=4,
    )).model_dump()


@router.get("/command/sample")
async def command_sample():
    return score_command(CommandInput(
        strike_rate=66,
        first_pitch_strike_rate=64,
        walk_rate=6.8,
        zone_rate=44,
        edge_rate=43,
        heart_rate=22,
        release_consistency_score=62,
    )).model_dump()


@router.get("/contact/sample")
async def contact_sample():
    return score_contact_management(ContactManagementInput(
        xera=3.55,
        fip=3.75,
        hard_hit_rate=37,
        barrel_rate=6.8,
        ground_ball_rate=45,
        fly_ball_rate=34,
        home_run_rate=0.95,
    )).model_dump()


@router.get("/fatigue/sample")
async def fatigue_sample():
    return score_pitcher_fatigue(FatigueInput(
        days_rest=5,
        pitches_last_start=91,
        pitches_last_7_days=91,
        pitches_last_30_days=390,
        velocity_delta_30d=0.2,
        spin_delta_30d=15,
        release_drift_score=66,
    )).model_dump()


@router.get("/matchup/sample")
async def matchup_sample():
    return score_pitcher_matchup(MatchupInput(
        opponent_fastball_run_value=-2,
        opponent_breaking_ball_run_value=1,
        opponent_offspeed_run_value=-1,
        opponent_whiff_rate=25,
        opponent_chase_rate=30,
        opponent_platoon_advantage_score=48,
        projected_lineup_hand_balance_score=52,
    )).model_dump()


@router.get("/starter/sample")
async def starter_sample():
    return calculate_starting_pitcher_intelligence(StartingPitcherIntelligenceInput(
        arsenal=PitchArsenalInput(fastball_velocity=95.2, velocity_delta_30d=0.4, fastball_run_value=-3, slider_run_value=-5, whiff_rate=29, chase_rate=32, pitch_mix_depth=4),
        command=CommandInput(strike_rate=66, first_pitch_strike_rate=64, walk_rate=6.8, zone_rate=44, edge_rate=43, heart_rate=22, release_consistency_score=62),
        contact=ContactManagementInput(xera=3.55, fip=3.75, hard_hit_rate=37, barrel_rate=6.8, ground_ball_rate=45, home_run_rate=0.95),
        fatigue=FatigueInput(days_rest=5, pitches_last_start=91, pitches_last_30_days=390, velocity_delta_30d=0.2, release_drift_score=66),
        matchup=MatchupInput(opponent_fastball_run_value=-2, opponent_breaking_ball_run_value=1, opponent_whiff_rate=25, opponent_chase_rate=30, opponent_platoon_advantage_score=48),
    )).model_dump()
