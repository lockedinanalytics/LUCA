from luca.decision.nfl.engine import make_nfl_unified_decision
from luca.decision.nfl.models import NflUnifiedDecisionInput
from luca.simulation.nfl.engine import simulate_nfl_game
from luca.simulation.nfl.models import NflSimulationInput


def test_nfl_simulation_bounds():
    result = simulate_nfl_game(NflSimulationInput(game_id="g1", home_offense_score=58, away_offense_score=51, home_defense_score=55, away_defense_score=50, runs=1000), spread=-3, total=45.5)
    assert 0 <= result.home_win_probability <= 1
    assert result.projected_total > 0


def test_nfl_unified_decision():
    result = make_nfl_unified_decision(NflUnifiedDecisionInput(
        game_id="g1",
        market_type="spread",
        selection="Home",
        odds=-110,
        spread=-3.0,
        total=45.5,
        quarterback_score=62,
        trench_score=58,
        skill_coverage_score=59,
        context_score=56,
        market_score=57,
        defense_score=55,
        injury_score=54,
    ))
    assert 0 <= result.luca_score <= 100
    assert 0 <= result.projected_probability <= 1
    assert result.recommendation_tier in {"strong", "playable", "lean", "pass"}
