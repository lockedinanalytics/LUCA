from __future__ import annotations
from typing import List
from luca.core.models import MarketLine, MarketType, Sport, TeamGame
from luca.providers.base import MarketProvider, ScheduleProvider

class StaticScheduleProvider(ScheduleProvider):
    def get_games(self, sport: Sport, league: str, date: str) -> List[TeamGame]:
        return [TeamGame(game_id=f"{sport.value}-{date}-001", sport=sport, league=league, date=date, away_team="Away Sample", home_team="Home Sample", venue="Sample Venue")]

class StaticMarketProvider(MarketProvider):
    def get_markets(self, games: List[TeamGame]) -> List[MarketLine]:
        rows = []
        for g in games:
            rows += [
                MarketLine(game_id=g.game_id, market_type=MarketType.MONEYLINE, selection=g.home_team, book="static", current_odds=-110),
                MarketLine(game_id=g.game_id, market_type=MarketType.SPREAD, selection=g.home_team, book="static", spread=-1.5, current_odds=-110),
                MarketLine(game_id=g.game_id, market_type=MarketType.TOTAL, selection="over", book="static", total=8.5, current_odds=-110),
            ]
        return rows
