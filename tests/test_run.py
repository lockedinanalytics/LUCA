from luca.core.models import Sport
from luca.providers.static.provider import StaticMarketProvider, StaticScheduleProvider
from luca.run.orchestrator import run_luca_for_sport
from luca.contests.circa_survivor.engine import SurvivorTeamOption, rank_survivor_options


def test_run_luca_static_nfl():
    result = run_luca_for_sport(
        sport=Sport.NFL,
        league="NFL",
        date="2026-08-01",
        schedule_provider=StaticScheduleProvider(),
        market_provider=StaticMarketProvider(),
    )
    assert result.games_evaluated == 1


def test_survivor_rank():
    result = rank_survivor_options([
        SurvivorTeamOption(team="BUF", win_probability=0.78, future_value=88, ownership_projection=32, scarcity_score=70, schedule_path_value=82, risk_stability=76)
    ])
    assert result[0].team == "BUF"
