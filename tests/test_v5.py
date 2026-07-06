from luca.simulation.engine import simulate_game
from luca.simulation.models import SimulationRequest
from luca.validation.completeness import validate_required_fields
from luca.database.sqlite_repo import SqliteLedgerRepository


def test_simulation_runs():
    result = simulate_game(SimulationRequest(game_id="x", runs=100, mean_home=4.5, mean_away=4.0))
    assert result.runs == 100
    assert 0 <= result.home_win_probability <= 1


def test_completeness():
    report = validate_required_fields({"a": 1, "b": None}, ["a", "b"])
    assert report.completeness == 0.5


def test_sqlite_repo_init(tmp_path):
    repo = SqliteLedgerRepository(str(tmp_path / "test.sqlite3"))
    assert repo.list_decisions() == []
