from __future__ import annotations

from pydantic import BaseModel, Field


class NflUnifiedDecisionInput(BaseModel):
    sport: str = "nfl"
    league: str = "NFL"
    game_id: str
    home_team: str = "Home"
    away_team: str = "Away"
    market_type: str = "moneyline"
    selection: str = "Home"
    odds: float = -110
    spread: float | None = None
    total: float | None = None
    quarterback_score: float = 50.0
    trench_score: float = 50.0
    skill_coverage_score: float = 50.0
    context_score: float = 50.0
    market_score: float = 50.0
    defense_score: float = 50.0
    injury_score: float = 50.0
    home_field_edge: float = 1.8


class NflUnifiedDecisionOutput(BaseModel):
    game_id: str
    selection: str
    market_type: str
    luca_score: float
    projected_probability: float
    confidence: float
    expected_value: float | None
    recommendation_tier: str
    suggested_units: float
    simulation: dict
    explainability: dict[str, float] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)
