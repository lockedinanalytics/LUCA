from luca.core.models import Sport
from luca.providers.static.provider import StaticMarketProvider, StaticScheduleProvider
from luca.run.orchestrator import run_luca_for_sport
from luca.simulation.engine import SimulationRequest, simulate_game

def test_static_run():
    result=run_luca_for_sport(Sport.NFL,"NFL","2026-08-01",StaticScheduleProvider(),StaticMarketProvider())
    assert result.games_evaluated == 1

def test_simulation():
    row=simulate_game(SimulationRequest(game_id="x", runs=100))
    assert 0 <= row["home_win_probability"] <= 1
