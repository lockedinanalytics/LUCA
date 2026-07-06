from luca.results.grader import FinalResult, grade_decision
from luca.ledger.models import LedgerDecision
from luca.providers.freshness.models import freshness_report
from luca.units.engine import assign_units


def test_grade_decision_win():
    d = LedgerDecision(
        decision_id="d1",
        game_id="g1",
        date="2026-08-01",
        sport="nfl",
        league="NFL",
        category="cabinet",
        market="moneyline",
        selection="Home",
        odds=-110,
        units=1.0,
        confidence=80,
    )
    result = grade_decision(d, FinalResult(game_id="g1", final_score="Home 24, Away 17", winner="Home"))
    assert result.result == "win"


def test_freshness_missing():
    report = freshness_report("x", None, 300)
    assert report.status == "missing"


def test_assign_units_no_ev():
    decision = assign_units(90, expected_value=-0.01)
    assert decision.official_units == 0
