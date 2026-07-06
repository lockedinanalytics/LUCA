from __future__ import annotations

from pydantic import BaseModel, Field


class ReceiverUnitInput(BaseModel):
    separation_score: float | None = None
    target_share_score: float | None = None
    route_participation_score: float | None = None
    explosive_route_score: float | None = None
    contested_catch_score: float | None = None
    yards_after_catch_score: float | None = None
    slot_efficiency_score: float | None = None
    boundary_efficiency_score: float | None = None
    injury_penalty: float = 0.0
    depth_score: float | None = None


class ReceiverUnitOutput(BaseModel):
    separation_score: float
    utilization_score: float
    explosive_skill_score: float
    possession_skill_score: float
    depth_health_score: float
    final_receiver_score: float
    warnings: list[str] = Field(default_factory=list)


class TightEndInput(BaseModel):
    route_rate_score: float | None = None
    yards_per_route_score: float | None = None
    red_zone_usage_score: float | None = None
    blocking_support_score: float | None = None
    linebacker_matchup_score: float | None = None
    safety_matchup_score: float | None = None


class TightEndOutput(BaseModel):
    receiving_matchup_score: float
    red_zone_score: float
    formation_flex_score: float
    final_te_score: float
    warnings: list[str] = Field(default_factory=list)


class RunningBackInput(BaseModel):
    rushing_efficiency_score: float | None = None
    receiving_utilization_score: float | None = None
    pass_protection_score: float | None = None
    explosive_run_score: float | None = None
    yards_after_contact_score: float | None = None
    vision_score: float | None = None
    goal_line_usage_score: float | None = None


class RunningBackOutput(BaseModel):
    rushing_value_score: float
    receiving_value_score: float
    protection_value_score: float
    goal_line_value_score: float
    final_rb_score: float
    warnings: list[str] = Field(default_factory=list)


class CoverageUnitInput(BaseModel):
    man_coverage_score: float | None = None
    zone_coverage_score: float | None = None
    pressure_coverage_synergy_score: float | None = None
    explosive_pass_prevention_score: float | None = None
    slot_coverage_score: float | None = None
    boundary_coverage_score: float | None = None
    safety_help_score: float | None = None
    linebacker_coverage_score: float | None = None
    injury_penalty: float = 0.0
    communication_score: float | None = None


class CoverageUnitOutput(BaseModel):
    coverage_quality_score: float
    explosive_prevention_score: float
    matchup_flexibility_score: float
    communication_health_score: float
    final_coverage_score: float
    warnings: list[str] = Field(default_factory=list)


class SkillCoverageMatchupInput(BaseModel):
    receivers: ReceiverUnitInput = Field(default_factory=ReceiverUnitInput)
    tight_end: TightEndInput = Field(default_factory=TightEndInput)
    running_back: RunningBackInput = Field(default_factory=RunningBackInput)
    coverage: CoverageUnitInput = Field(default_factory=CoverageUnitInput)
    quarterback_accuracy_score: float = 50.0
    pass_protection_score: float = 50.0
    offensive_scheme_score: float = 50.0
    defensive_scheme_score: float = 50.0


class SkillCoverageMatchupOutput(BaseModel):
    receiver_score: float
    tight_end_score: float
    running_back_score: float
    coverage_score: float
    wr_cb_matchup_score: float
    te_matchup_score: float
    rb_matchup_score: float
    explosive_pass_projection: float
    possession_chain_score: float
    red_zone_skill_score: float
    final_skill_coverage_score: float
    confidence: float
    warnings: list[str] = Field(default_factory=list)
    explainability: dict[str, float] = Field(default_factory=dict)
