from luca.core.models import MarketLine, MarketType
from luca.markets.evaluator import evaluate_market
from luca.scoring.run_expectation import TeamProjection, project_game_total


def test_market_moneyline():
    line = MarketLine(game_id="g1", market_type=MarketType.MONEYLINE, selection="Home", current_odds=-110)
    row = evaluate_market(line, projected_probability=0.58)
    assert row.market == "moneyline"


def test_team_projection_total():
    total = project_game_total(
        TeamProjection(team="H", baseline_points=24, offensive_score=60),
        TeamProjection(team="A", baseline_points=21, offensive_score=55),
    )
    assert total > 0
