from __future__ import annotations

from pydantic import BaseModel, Field


class PitchArsenalInput(BaseModel):
    fastball_velocity: float | None = None
    velocity_delta_30d: float | None = None
    fastball_run_value: float | None = None
    slider_run_value: float | None = None
    curveball_run_value: float | None = None
    changeup_run_value: float | None = None
    cutter_run_value: float | None = None
    splitter_run_value: float | None = None
    whiff_rate: float | None = None
    chase_rate: float | None = None
    called_strike_rate: float | None = None
    pitch_mix_depth: int | None = None


class PitchArsenalOutput(BaseModel):
    velocity_score: float
    stuff_score: float
    deception_score: float
    arsenal_depth_score: float
    final_arsenal_score: float
    notes: list[str] = Field(default_factory=list)


class CommandInput(BaseModel):
    strike_rate: float | None = None
    first_pitch_strike_rate: float | None = None
    walk_rate: float | None = None
    zone_rate: float | None = None
    edge_rate: float | None = None
    heart_rate: float | None = None
    release_consistency_score: float | None = None


class CommandOutput(BaseModel):
    zone_control_score: float
    count_leverage_score: float
    mistake_avoidance_score: float
    final_command_score: float
    notes: list[str] = Field(default_factory=list)


class ContactManagementInput(BaseModel):
    xera: float | None = None
    fip: float | None = None
    hard_hit_rate: float | None = None
    barrel_rate: float | None = None
    ground_ball_rate: float | None = None
    fly_ball_rate: float | None = None
    home_run_rate: float | None = None


class ContactManagementOutput(BaseModel):
    damage_suppression_score: float
    batted_ball_shape_score: float
    regression_score: float
    final_contact_score: float
    notes: list[str] = Field(default_factory=list)


class FatigueInput(BaseModel):
    days_rest: int | None = None
    pitches_last_start: int | None = None
    pitches_last_7_days: int | None = None
    pitches_last_30_days: int | None = None
    velocity_delta_30d: float | None = None
    spin_delta_30d: float | None = None
    release_drift_score: float | None = None


class FatigueOutput(BaseModel):
    workload_score: float
    recovery_score: float
    signal_stability_score: float
    final_fatigue_score: float
    notes: list[str] = Field(default_factory=list)


class MatchupInput(BaseModel):
    opponent_fastball_run_value: float | None = None
    opponent_breaking_ball_run_value: float | None = None
    opponent_offspeed_run_value: float | None = None
    opponent_whiff_rate: float | None = None
    opponent_chase_rate: float | None = None
    opponent_platoon_advantage_score: float | None = None
    projected_lineup_hand_balance_score: float | None = None


class MatchupOutput(BaseModel):
    pitch_type_fit_score: float
    bat_missing_fit_score: float
    platoon_fit_score: float
    final_matchup_score: float
    notes: list[str] = Field(default_factory=list)


class StartingPitcherIntelligenceInput(BaseModel):
    arsenal: PitchArsenalInput = Field(default_factory=PitchArsenalInput)
    command: CommandInput = Field(default_factory=CommandInput)
    contact: ContactManagementInput = Field(default_factory=ContactManagementInput)
    fatigue: FatigueInput = Field(default_factory=FatigueInput)
    matchup: MatchupInput = Field(default_factory=MatchupInput)


class StartingPitcherIntelligenceOutput(BaseModel):
    arsenal_score: float
    command_score: float
    contact_score: float
    fatigue_score: float
    matchup_score: float
    final_sp_score: float
    confidence: float
    warnings: list[str] = Field(default_factory=list)
    explainability: dict[str, float] = Field(default_factory=dict)
