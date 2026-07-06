from luca.core.models import MarketType, Sport
from luca.decision.engine import DecisionInput, make_decision
from luca.ev.engine import calculate_ev
from luca.risk.engine import RiskInput, calculate_risk
from luca.clv.engine import calculate_clv
from luca.market_tracking.models import MarketSnapshot
from luca.market_tracking.timeline import build_market_timelines
from luca.providers.static.provider import StaticMarketProvider, StaticScheduleProvider
from luca.run.orchestrator import run_luca_for_sport


def test_ev_positive():
    result = calculate_ev(0.58, -110)
    assert result.edge > 0


def test_risk_engine():
    result = calculate_risk(RiskInput(variance=2.0, data_completeness=0.8))
    assert result.risk_grade in {'low', 'medium', 'high', 'extreme'}


def test_decision_engine():
    result = make_decision(DecisionInput(
        sport=Sport.MLB,
        league='MLB',
        game_id='g1',
        market_type=MarketType.MONEYLINE,
        selection='Home',
        odds=-110,
        luca_score=88,
        projected_probability=0.58,
        confidence=84,
    ))
    assert result.pick.selection == 'Home'


def test_clv():
    result = calculate_clv(-110, -125)
    assert result.clv_points is not None


def test_market_timeline():
    rows = [
        MarketSnapshot(game_id='g1', market='moneyline', selection='Home', odds=-110, timestamp='open'),
        MarketSnapshot(game_id='g1', market='moneyline', selection='Home', odds=-125, timestamp='current'),
    ]
    timelines = build_market_timelines(rows)
    assert len(timelines) == 1


def test_run_integrated_simulation():
    result = run_luca_for_sport(Sport.NFL, 'NFL', '2026-08-01', StaticScheduleProvider(), StaticMarketProvider())
    assert result.evaluations[0].raw.get('simulation')
