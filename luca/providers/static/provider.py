from __future__ import annotations

from typing import List

from luca.core.models import MarketLine, MarketType, Sport, TeamGame
from luca.providers.base import MarketProvider, ScheduleProvider


class StaticScheduleProvider(ScheduleProvider):
    """Local provider used for tests, development, and Railway smoke checks."""

    def get_games(self, sport: Sport, league: str, date: str) -> List[TeamGame]:
        return [
            TeamGame(
                game_id=f"{sport.value}-{date}-001",
                sport=sport,
                league=league,
                date=date,
                away_team="Away Sample",
                home_team="Home Sample",
                venue="Sample Venue",
            )
        ]


class StaticMarketProvider(MarketProvider):
    def get_markets(self, games: List[TeamGame]) -> List[MarketLine]:
        markets: List[MarketLine] = []
        for game in games:
            markets.append(
                MarketLine(
                    game_id=game.game_id,
                    market_type=MarketType.MONEYLINE,
                    selection=game.home_team,
                    book="static",
                    current_odds=-110,
                )
            )
            markets.append(
                MarketLine(
                    game_id=game.game_id,
                    market_type=MarketType.SPREAD,
                    selection=game.home_team,
                    book="static",
                    spread=-1.5,
                    current_odds=-110,
                )
            )
            markets.append(
                MarketLine(
                    game_id=game.game_id,
                    market_type=MarketType.TOTAL,
                    selection="over",
                    book="static",
                    total=8.5,
                    current_odds=-110,
                )
            )
        return markets
