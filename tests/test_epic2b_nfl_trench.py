from luca.core.models import Sport, TeamGame
from luca.features.mappers.nfl.mapper import NflFeatureMapper
from luca.intelligence.nfl.trench.defensive_front import score_defensive_front
from luca.intelligence.nfl.trench.matchup import calculate_trench_matchup
from luca.intelligence.nfl.trench.models import DefensiveFrontInput, OffensiveLineInput, TrenchMatchupInput
from luca.intelligence.nfl.trench.offensive_line import score_offensive_line


def test_offensive_line_bounds():
    result = score_offensive_line(OffensiveLineInput(pass_block_win_rate=64, run_block_win_rate=72, pressure_allowed_rate=29))
    assert 0 <= result.final_ol_score <= 100


def test_defensive_front_bounds():
    result = score_defensive_front(DefensiveFrontInput(pressure_rate=37, run_stop_win_rate=33, missed_tackle_rate=9.5))
    assert 0 <= result.final_front_score <= 100


def test_trench_matchup_bounds():
    result = calculate_trench_matchup(TrenchMatchupInput(
        offensive_line=OffensiveLineInput(pass_block_win_rate=64, run_block_win_rate=72, pressure_allowed_rate=29),
        defensive_front=DefensiveFrontInput(pressure_rate=37, run_stop_win_rate=33, missed_tackle_rate=9.5),
    ))
    assert 0 <= result.final_trench_score <= 100
    assert result.confidence > 0


def test_nfl_mapper_accepts_trench_v2():
    game = TeamGame(game_id="g1", sport=Sport.NFL, league="NFL", date="2026-09-01", away_team="Away", home_team="Home")
    modules = NflFeatureMapper().build_modules(game, [], context={
        "trench_v2": {
            "offensive_line": {"pass_block_win_rate": 64, "run_block_win_rate": 72, "pressure_allowed_rate": 29},
            "defensive_front": {"pressure_rate": 37, "run_stop_win_rate": 33, "missed_tackle_rate": 9.5},
        }
    })
    assert "ol_dl_edge" in modules
    assert "pass_protection_edge" in modules
