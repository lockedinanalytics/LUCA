from luca.core.models import MarketLine, MarketType, Sport, TeamGame
from luca.providers.odds.the_odds_api.mapper import odds_event_to_market_lines
from luca.providers.odds.the_odds_api.provider import TheOddsApiMarketProvider
from luca.features.mappers.factory import get_feature_mapper


def test_odds_mapper_h2h():
    event = {
        "id": "event1",
        "home_team": "Home",
        "away_team": "Away",
        "bookmakers": [{
            "key": "draftkings",
            "markets": [{
                "key": "h2h",
                "outcomes": [{"name": "Home", "price": -110}, {"name": "Away", "price": 100}]
            }]
        }]
    }
    game = TeamGame(game_id="g1", sport=Sport.NFL, league="NFL", date="2026-08-01", away_team="Away", home_team="Home")
    lines = odds_event_to_market_lines(event, game)
    assert len(lines) == 2
    assert lines[0].market_type == MarketType.MONEYLINE


def test_odds_status_masks_key(monkeypatch):
    monkeypatch.setenv("ODDS_API_KEY", "abcdef123456")
    provider = TheOddsApiMarketProvider()
    status = provider.status()
    assert status.configured is True
    assert "3456" in status.details["key"]


def test_feature_mapper_mlb():
    game = TeamGame(game_id="g1", sport=Sport.MLB, league="MLB", date="2026-07-04", away_team="Away", home_team="Home")
    mapper = get_feature_mapper(Sport.MLB)
    scores = mapper.build_modules(game, [])
    assert "sp" in scores
