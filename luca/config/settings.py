from __future__ import annotations
from typing import Any, Dict
from pydantic import BaseModel, Field

class GovernanceSettings(BaseModel):
    min_data_completeness: float = 0.70
    min_confidence: float = 70.0
    high_risk_unit_cap: float = 0.75
    max_standard_units: float = 3.0

class EdgeSettings(BaseModel):
    moneyline_lean: float = 0.02
    moneyline_playable: float = 0.04
    moneyline_strong: float = 0.06
    spread_lean: float = 1.1
    spread_playable: float = 2.1
    spread_strong: float = 3.1
    total_lean: float = 0.5
    total_playable: float = 1.0
    total_strong: float = 2.0

class LucaSettings(BaseModel):
    model_version: str = "0.4.0"
    environment: str = "development"
    governance: GovernanceSettings = Field(default_factory=GovernanceSettings)
    edge: EdgeSettings = Field(default_factory=EdgeSettings)
    sport_weights: Dict[str, Dict[str, float]] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)

DEFAULT_SETTINGS = LucaSettings()
