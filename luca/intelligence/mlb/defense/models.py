from __future__ import annotations

from pydantic import BaseModel, Field


class CatcherInput(BaseModel):
    name: str = "Unknown Catcher"
    framing_score: float = 50.0
    blocking_score: float = 50.0
    throwing_score: float = 50.0
    pop_time_score: float = 50.0
    game_calling_score: float = 50.0
    pitcher_familiarity_score: float = 50.0
    workload_fatigue_score: float = 50.0
    availability_penalty: float = 0.0


class CatcherOutput(BaseModel):
    receiving_score: float
    run_game_control_score: float
    pitcher_support_score: float
    fatigue_adjusted_score: float
    final_cam_score: float
    warnings: list[str] = Field(default_factory=list)


class FieldingUnitInput(BaseModel):
    infield_oaa_score: float = 50.0
    outfield_oaa_score: float = 50.0
    drs_score: float = 50.0
    arm_strength_score: float = 50.0
    double_play_score: float = 50.0
    range_score: float = 50.0
    error_avoidance_score: float = 50.0
    positioning_score: float = 50.0


class FieldingUnitOutput(BaseModel):
    infield_support_score: float
    outfield_support_score: float
    throwing_support_score: float
    conversion_score: float
    final_fielding_score: float
    warnings: list[str] = Field(default_factory=list)


class BaserunnerPreventionInput(BaseModel):
    catcher_throwing_score: float = 50.0
    pitcher_hold_score: float = 50.0
    infield_tag_score: float = 50.0
    outfield_arm_score: float = 50.0
    opponent_steal_pressure_score: float = 50.0
    opponent_extra_base_pressure_score: float = 50.0


class BaserunnerPreventionOutput(BaseModel):
    steal_prevention_score: float
    extra_base_prevention_score: float
    pressure_adjusted_score: float
    warnings: list[str] = Field(default_factory=list)


class DefensiveIntelligenceInput(BaseModel):
    catcher: CatcherInput = Field(default_factory=CatcherInput)
    fielding: FieldingUnitInput = Field(default_factory=FieldingUnitInput)
    baserunner_prevention: BaserunnerPreventionInput = Field(default_factory=BaserunnerPreventionInput)
    pitcher_contact_profile_score: float = 50.0
    park_defensive_difficulty_score: float = 50.0


class DefensiveIntelligenceOutput(BaseModel):
    cam_score: float
    fielding_score: float
    baserunner_prevention_score: float
    contact_support_score: float
    defensive_run_prevention_score: float
    confidence: float
    warnings: list[str] = Field(default_factory=list)
    explainability: dict[str, float] = Field(default_factory=dict)
