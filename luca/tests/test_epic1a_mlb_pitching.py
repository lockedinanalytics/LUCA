from luca.intelligence.mlb.pitching.arsenal import score_pitch_arsenal
from luca.intelligence.mlb.pitching.command import score_command
from luca.intelligence.mlb.pitching.contact import score_contact_management
from luca.intelligence.mlb.pitching.fatigue import score_pitcher_fatigue
from luca.intelligence.mlb.pitching.matchup import score_pitcher_matchup
from luca.intelligence.mlb.pitching.engine import calculate_starting_pitcher_intelligence
from luca.intelligence.mlb.pitching.models import (
    PitchArsenalInput,
    CommandInput,
    ContactManagementInput,
    FatigueInput,
    MatchupInput,
    StartingPitcherIntelligenceInput,
)
from luca.core.models import Sport, TeamGame
from luca.features.mappers.mlb import MlbFeatureMapper


def test_arsenal_score_bounds():
    row = score_pitch_arsenal(PitchArsenalInput(fastball_velocity=96, velocity_delta_30d=0.5, slider_run_value=-4, whiff_rate=30, pitch_mix_depth=4))
    assert 0 <= row.final_arsenal_score <= 100


def test_command_score_bounds():
    row = score_command(CommandInput(strike_rate=66, walk_rate=6.5, first_pitch_strike_rate=63, heart_rate=22))
    assert 0 <= row.final_command_score <= 100


def test_contact_score_bounds():
    row = score_contact_management(ContactManagementInput(xera=3.6, fip=3.8, hard_hit_rate=37, barrel_rate=7))
    assert 0 <= row.final_contact_score <= 100


def test_fatigue_score_bounds():
    row = score_pitcher_fatigue(FatigueInput(days_rest=5, pitches_last_start=92, velocity_delta_30d=0.2))
    assert 0 <= row.final_fatigue_score <= 100


def test_matchup_score_bounds():
    row = score_pitcher_matchup(MatchupInput(opponent_whiff_rate=26, opponent_chase_rate=30, opponent_platoon_advantage_score=48))
    assert 0 <= row.final_matchup_score <= 100


def test_starting_pitcher_intelligence_output():
    result = calculate_starting_pitcher_intelligence(StartingPitcherIntelligenceInput(
        arsenal=PitchArsenalInput(fastball_velocity=95.2, slider_run_value=-5, whiff_rate=29, pitch_mix_depth=4),
        command=CommandInput(strike_rate=66, walk_rate=6.8, first_pitch_strike_rate=64),
        contact=ContactManagementInput(xera=3.55, fip=3.75, hard_hit_rate=37, barrel_rate=6.8),
        fatigue=FatigueInput(days_rest=5, pitches_last_start=91, velocity_delta_30d=0.2),
        matchup=MatchupInput(opponent_whiff_rate=25, opponent_chase_rate=30),
    ))
    assert result.final_sp_score > 0
    assert result.confidence > 50


def test_mlb_mapper_accepts_pitching_v2_context():
    game = TeamGame(game_id="g1", sport=Sport.MLB, league="MLB", date="2026-07-04", away_team="Away", home_team="Home")
    mapper = MlbFeatureMapper()
    modules = mapper.build_modules(game, [], context={
        "starting_pitcher_v2": {
            "arsenal": {"fastball_velocity": 95.2, "slider_run_value": -5, "whiff_rate": 29, "pitch_mix_depth": 4},
            "command": {"strike_rate": 66, "walk_rate": 6.8},
            "contact": {"xera": 3.55, "fip": 3.75, "hard_hit_rate": 37},
            "fatigue": {"days_rest": 5, "pitches_last_start": 91},
            "matchup": {"opponent_whiff_rate": 25}
        }
    })
    assert "sp" in modules
    assert modules["sp"] > 0
