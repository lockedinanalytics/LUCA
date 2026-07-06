from __future__ import annotations

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "LUCA Universal Decision Operating System"
    model_version: str = "1.0.0-phase2"
    environment: str = "development"

    # Storage
    ledger_backend: str = "sqlite"
    sqlite_path: str = "luca.sqlite3"
    json_ledger_path: str = "luca_ledger.jsonl"

    # Governance
    min_data_completeness: float = 0.70
    min_confidence: float = 70.0
    max_standard_units: float = 3.0
    high_risk_unit_cap: float = 0.75

    # Provider selection
    schedule_provider: str = "static"
    market_provider: str = "static"
    weather_provider: str = "null"
    injury_provider: str = "null"

    # The Odds API
    odds_api_key: str | None = None
    odds_api_base_url: str = "https://api.the-odds-api.com/v4"
    odds_api_regions: str = "us"
    odds_api_markets: str = "h2h,spreads,totals"
    odds_api_odds_format: str = "american"
    odds_api_date_format: str = "iso"

    # MLB Stats API
    mlb_stats_api_base_url: str = "https://statsapi.mlb.com/api/v1"

    # Provider safety
    provider_timeout_seconds: float = 20.0
    allow_live_network_calls: bool = False


@lru_cache
def get_settings() -> Settings:
    return Settings()
