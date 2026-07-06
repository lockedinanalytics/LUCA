from __future__ import annotations

from pydantic import BaseModel


class MlbLineupSnapshot(BaseModel):
    game_id: str
    home_lineup: list[str]
    away_lineup: list[str]
    home_probable_pitcher: str | None = None
    away_probable_pitcher: str | None = None


class MlbBoxscoreFeatures(BaseModel):
    game_id: str
    home_lineup_count: int
    away_lineup_count: int
    home_pitcher_count: int
    away_pitcher_count: int
    extraction_warnings: list[str] = []
