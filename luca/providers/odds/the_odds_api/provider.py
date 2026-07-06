from __future__ import annotations

from typing import List

from luca.config.settings import get_settings
from luca.core.models import MarketLine, Sport, TeamGame
from luca.providers.aliases.resolver import TeamAliasResolver
from luca.providers.base import MarketProvider
from luca.providers.odds.models import OddsProviderStatus
from luca.providers.odds.the_odds_api.client import TheOddsApiClient
from luca.providers.odds.the_odds_api.mapper import odds_event_to_market_lines
from luca.security.secrets import mask_secret


SPORT_KEY_MAP = {
    Sport.MLB: "baseball_mlb",
    Sport.NFL: "americanfootball_nfl",
    Sport.NCAAF: "americanfootball_ncaaf",
    Sport.NBA: "basketball_nba",
    Sport.NHL: "icehockey_nhl",
    Sport.SOCCER: "soccer_epl",
    Sport.MMA: "mma_mixed_martial_arts",
}


class TheOddsApiMarketProvider(MarketProvider):
    def __init__(self):
        self.settings = get_settings()
        self.resolver = TeamAliasResolver()

    def status(self) -> OddsProviderStatus:
        return OddsProviderStatus(
            provider="the_odds_api",
            configured=bool(self.settings.odds_api_key),
            live_enabled=self.settings.allow_live_network_calls,
            details={
                "regions": self.settings.odds_api_regions,
                "markets": self.settings.odds_api_markets,
                "key": mask_secret(self.settings.odds_api_key),
            },
        )

    def get_markets(self, games: List[TeamGame]) -> List[MarketLine]:
        if not games:
            return []

        sport_key = SPORT_KEY_MAP.get(games[0].sport)
        if not sport_key:
            return []

        client = TheOddsApiClient()
        events = client.get_odds(sport_key=sport_key)

        output: list[MarketLine] = []
        for game in games:
            event = self._match_event(game, events)
            if event:
                output.extend(odds_event_to_market_lines(event, game=game))
        return output

    def _match_event(self, game: TeamGame, events: list[dict]) -> dict | None:
        for event in events:
            event_home = event.get("home_team", "")
            event_away = event.get("away_team", "")
            home_match = self.resolver.same_team(event_home, game.home_team, game.sport.value, game.league)
            away_match = self.resolver.same_team(event_away, game.away_team, game.sport.value, game.league)
            if home_match and away_match:
                return event
        return None
