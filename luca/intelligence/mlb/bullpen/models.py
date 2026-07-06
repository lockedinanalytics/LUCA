from __future__ import annotations

from pydantic import BaseModel, Field


class RelieverUsageInput(BaseModel):
    name: str
    role: str = "middle"
    pitches_yesterday: int = 0
    pitches_last_3_days: int = 0
    appearances_last_3_days: int = 0
    back_to_back: bool = False
    three_in_four: bool = False
    available_override: bool | None = None
    leverage_role_score: float = 50.0
    season_quality_score: float = 50.0
    recent_quality_score: float = 50.0
    inherited_runner_score: float = 50.0
    command_volatility_score: float = 50.0


class RelieverAvailabilityOutput(BaseModel):
    name: str
    role: str
    availability_score: float
    fatigue_score: float
    quality_score: float
    leverage_score: float
    usable: bool
    warnings: list[str] = Field(default_factory=list)


class BullpenHierarchyInput(BaseModel):
    relievers: list[RelieverUsageInput] = Field(default_factory=list)


class BullpenHierarchyOutput(BaseModel):
    closer_score: float
    setup_score: float
    lefty_score: float
    long_relief_score: float
    depth_score: float
    available_high_leverage_count: int
    available_total_count: int
    warnings: list[str] = Field(default_factory=list)


class BullpenCollapseInput(BaseModel):
    available_total_count: int
    available_high_leverage_count: int
    bullpen_quality_score: float
    fatigue_score: float
    command_volatility_score: float
    inherited_runner_score: float
    manager_usage_score: float = 50.0


class BullpenCollapseOutput(BaseModel):
    collapse_probability_score: float
    multi_run_inning_risk: float
    command_risk: float
    leverage_gap_risk: float
    notes: list[str] = Field(default_factory=list)


class BullpenIntelligenceInput(BaseModel):
    relievers: list[RelieverUsageInput] = Field(default_factory=list)
    manager_usage_score: float = 50.0
    game_leverage_projection: float = 50.0


class BullpenIntelligenceOutput(BaseModel):
    availability_score: float
    fatigue_score: float
    quality_score: float
    leverage_score: float
    hierarchy_score: float
    collapse_risk_score: float
    final_bsi: float
    confidence: float
    warnings: list[str] = Field(default_factory=list)
    explainability: dict[str, float] = Field(default_factory=dict)
