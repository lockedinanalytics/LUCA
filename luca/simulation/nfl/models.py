from __future__ import annotations

from pydantic import BaseModel, Field


class NflSimulationInput(BaseModel):
    game_id: str
    home_team: str = "Home"
    away_team: str = "Away"
    home_offense_score: float = 50.0
    away_offense_score: float = 50.0
    home_defense_score: float = 50.0
    away_defense_score: float = 50.0
    home_context_score: float = 50.0
    away_context_score: float = 50.0
    home_market_score: float = 50.0
    away_market_score: float = 50.0
    total_baseline: float = 44.0
    home_field_edge: float = 1.8
    runs: int = 20000


class NflSimulationOutput(BaseModel):
    game_id: str
    home_win_probability: float
    away_win_probability: float
    projected_home_score: float
    projected_away_score: float
    projected_total: float
    projected_margin: float
    spread_cover_probability: float | None = None
    over_probability: float | None = None
    total_variance: float
    margin_variance: float
    confidence_interval_total: tuple[float, float]
    confidence_interval_margin: tuple[float, float]
    top_score_bands: dict[str, float] = Field(default_factory=dict)
