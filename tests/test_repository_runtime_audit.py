import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

import main
from luca.contests.circa_survivor.engine import (
    SurvivorTeamOption,
    rank_survivor_options,
)
from luca.core.models import MarketLine, MarketType, Sport, TeamGame
from luca.run.registry import get_sport_engine


@pytest.mark.parametrize("sport", tuple(Sport))
def test_every_registered_sport_engine_executes_deterministically(sport: Sport):
    game = TeamGame(
        game_id=f"audit-{sport.value}",
        sport=sport,
        league=sport.value.upper(),
        date="2026-08-24",
        away_team="Away",
        home_team="Home",
    )
    market = MarketLine(
        game_id=game.game_id,
        market_type=MarketType.MONEYLINE,
        selection=game.home_team,
        current_odds=-110,
    )

    first = get_sport_engine(sport).evaluate_games([game], [market])
    second = get_sport_engine(sport).evaluate_games([game], [market])

    assert first.sport is sport
    assert first.games_evaluated == 1
    assert len(first.evaluations) == 1
    assert first.model_dump(mode="json") == second.model_dump(mode="json")


@pytest.mark.parametrize(
    ("field", "value"),
    (
        ("win_probability", 1.01),
        ("future_value", 101),
        ("ownership_projection", -1),
        ("scarcity_score", 101),
        ("schedule_path_value", -1),
        ("risk_stability", 101),
    ),
)
def test_circa_survivor_rejects_impossible_evidence(field: str, value: float):
    payload = {
        "team": "BUF",
        "win_probability": 0.78,
        "future_value": 88,
        "ownership_projection": 32,
        "scarcity_score": 70,
        "schedule_path_value": 82,
        "risk_stability": 76,
    }
    payload[field] = value

    with pytest.raises(ValidationError):
        SurvivorTeamOption(**payload)


def test_circa_survivor_ranking_is_descending():
    results = rank_survivor_options(
        [
            SurvivorTeamOption(
                team="BUF",
                win_probability=0.78,
                future_value=88,
                ownership_projection=32,
                scarcity_score=70,
                schedule_path_value=82,
                risk_stability=76,
            ),
            SurvivorTeamOption(
                team="MIN",
                win_probability=0.70,
                future_value=62,
                ownership_projection=12,
                scarcity_score=82,
                schedule_path_value=68,
                risk_stability=70,
            ),
        ]
    )

    assert [row.survivor_score for row in results] == sorted(
        (row.survivor_score for row in results), reverse=True
    )


def test_main_registers_each_debug_route_once():
    paths = [route.path for route in main.app.routes]

    assert paths.count("/debug/pitcher/{pitcher_id}") == 1


def test_run_luca_returns_non_success_when_execution_raises(monkeypatch):
    def fail(*args, **kwargs):
        raise RuntimeError("provider exploded")

    monkeypatch.setattr(main, "run_luca_for_sport", fail)

    response = TestClient(main.app).get("/run-luca/mlb?date=2026-08-24")

    assert response.status_code == 502
    assert response.json()["detail"]["error_type"] == "RuntimeError"
