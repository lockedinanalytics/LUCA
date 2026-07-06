from __future__ import annotations

from typing import Any, Dict
from pydantic import BaseModel, Field


class SimulationRequest(BaseModel):
    game_id: str
    runs: int = 10000
    mean_home: float = 4.5
    mean_away: float = 4.2
    metadata: Dict[str, Any] = Field(default_factory=dict)


class SimulationResult(BaseModel):
    game_id: str
    runs: int
    home_win_probability: float
    away_win_probability: float
    projected_home_score: float
    projected_away_score: float
    projected_total: float
    projected_margin: float
    variance: float
    entropy: float
    distribution: Dict[str, float] = Field(default_factory=dict)
