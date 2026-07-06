from luca.core.models import LucaRunResult, Sport
from luca.providers.base import MarketProvider, ScheduleProvider
from luca.run.registry import get_sport_engine

def run_luca_for_sport(sport: Sport, league: str, date: str, schedule_provider: ScheduleProvider, market_provider: MarketProvider) -> LucaRunResult:
    games = schedule_provider.get_games(sport, league, date)
    markets = market_provider.get_markets(games)
    return get_sport_engine(sport).evaluate_games(games, markets)
