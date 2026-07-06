from __future__ import annotations

from pydantic import BaseModel, Field


class OffensiveLineInput(BaseModel):
    pass_block_win_rate: float | None = None
    run_block_win_rate: float | None = None
    pressure_allowed_rate: float | None = None
    sack_responsibility_rate: float | None = None
    blitz_pickup_score: float | None = None
    interior_protection_score: float | None = None
    edge_protection_score: float | None = None
    short_yardage_score: float | None = None
    goal_line_blocking_score: float | None = None
    continuity_score: float | None = None
    injury_penalty: float = 0.0
    depth_quality_score: float | None = None
    fatigue_penalty: float = 0.0


class OffensiveLineOutput(BaseModel):
    pass_protection_score: float
    run_blocking_score: float
    continuity_health_score: float
    short_yardage_score: float
    final_ol_score: float
    warnings: list[str] = Field(default_factory=list)


class DefensiveFrontInput(BaseModel):
    pressure_rate: float | None = None
    quick_pressure_rate: float | None = None
    sack_conversion_rate: float | None = None
    pass_rush_win_rate: float | None = None
    run_stop_win_rate: float | None = None
    stuff_rate: float | None = None
    missed_tackle_rate: float | None = None
    gap_integrity_score: float | None = None
    edge_containment_score: float | None = None
    interior_disruption_score: float | None = None
    rotation_depth_score: float | None = None
    fatigue_penalty: float = 0.0


class DefensiveFrontOutput(BaseModel):
    pass_rush_score: float
    run_defense_score: float
    disruption_score: float
    containment_score: float
    final_front_score: float
    warnings: list[str] = Field(default_factory=list)


class TrenchMatchupInput(BaseModel):
    offensive_line: OffensiveLineInput = Field(default_factory=OffensiveLineInput)
    defensive_front: DefensiveFrontInput = Field(default_factory=DefensiveFrontInput)
    quarterback_pressure_resilience_score: float = 50.0
    running_back_vision_score: float = 50.0
    offensive_scheme_score: float = 50.0
    defensive_scheme_score: float = 50.0
    weather_surface_score: float = 50.0


class TrenchMatchupOutput(BaseModel):
    offensive_line_score: float
    defensive_front_score: float
    pass_protection_edge: float
    run_blocking_edge: float
    pressure_projection_score: float
    sack_projection_score: float
    rushing_efficiency_projection: float
    explosive_run_probability_score: float
    short_yardage_advantage_score: float
    red_zone_trench_score: float
    final_trench_score: float
    confidence: float
    warnings: list[str] = Field(default_factory=list)
    explainability: dict[str, float] = Field(default_factory=dict)
