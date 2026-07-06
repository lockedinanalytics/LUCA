from __future__ import annotations

from luca.config.settings import get_settings
from luca.providers.base import MarketProvider, ScheduleProvider
from luca.providers.mlb.statsapi import MlbStatsApiScheduleProvider
from luca.providers.odds.the_odds_api.provider import TheOddsApiMarketProvider
from luca.providers.static.provider import StaticMarketProvider, StaticScheduleProvider


def get_schedule_provider(name: str | None = None) -> ScheduleProvider:
    settings = get_settings()
    selected = (name or settings.schedule_provider).lower()
    if selected == "mlb_stats_api":
        return MlbStatsApiScheduleProvider()
    return StaticScheduleProvider()


def get_market_provider(name: str | None = None) -> MarketProvider:
    settings = get_settings()
    selected = (name or settings.market_provider).lower()
    if selected in {"odds_api", "the_odds_api"}:
        return TheOddsApiMarketProvider()
    return StaticMarketProvider()
