from __future__ import annotations
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    app_name: str = "LUCA Universal Decision Operating System"
    model_version: str = "1.0.0-phase1"
    environment: str = "development"
    ledger_backend: str = "sqlite"
    sqlite_path: str = "luca.sqlite3"
    json_ledger_path: str = "luca_ledger.jsonl"
    min_data_completeness: float = 0.70
    min_confidence: float = 70.0
    max_standard_units: float = 3.0
    high_risk_unit_cap: float = 0.75

@lru_cache
def get_settings() -> Settings:
    return Settings()
