from __future__ import annotations

from pydantic import BaseModel, Field


class NflQuarterbackEfficiencyInput(BaseModel):
    epa_per_play: float | None = None
    success_rate: float | None = None
    cpoe: float | None = None
    anya: float | None = None
    third_down_success_rate: float | None = None
    red_zone_efficiency: float | None = None


class NflQuarterbackExplosiveInput(BaseModel):
    explosive_pass_rate: float | None = None
    air_yards_per_attempt: float | None = None
    big_time_throw_rate: float | None = None
    deep_ball_accuracy_score: float | None = None
    yards_after_catch_creation_score: float | None = None


class NflQuarterbackPressureInput(BaseModel):
    pressure_epa_per_play: float | None = None
    pressure_to_sack_rate: float | None = None
    blitz_epa_per_play: float | None = None
    clean_pocket_epa_per_play: float | None = None
    time_to_throw: float | None = None


class NflQuarterbackDecisionInput(BaseModel):
    turnover_worthy_play_rate: float | None = None
    interception_rate: float | None = None
    sack_avoidance_score: float | None = None
    checkdown_efficiency_score: float | None = None
    late_down_decision_score: float | None = None


class NflQuarterbackMobilityInput(BaseModel):
    scramble_epa: float | None = None
    designed_run_epa: float | None = None
    pressure_escape_score: float | None = None
    rushing_success_rate: float | None = None


class NflQuarterbackSituationalInput(BaseModel):
    two_minute_score: float | None = None
    comeback_score: float | None = None
    home_away_split_score: float | None = None
    indoor_outdoor_split_score: float | None = None
    weather_sensitivity_score: float | None = None
    injury_penalty: float = 0.0
    fatigue_penalty: float = 0.0


class NflQuarterbackMatchupInput(BaseModel):
    opponent_pressure_score: float = 50.0
    opponent_coverage_score: float = 50.0
    opponent_blitz_rate_score: float = 50.0
    offensive_line_support_score: float = 50.0
    receiver_separation_score: float = 50.0
    coaching_pass_design_score: float = 50.0


class NflQuarterbackIntelligenceInput(BaseModel):
    efficiency: NflQuarterbackEfficiencyInput = Field(default_factory=NflQuarterbackEfficiencyInput)
    explosive: NflQuarterbackExplosiveInput = Field(default_factory=NflQuarterbackExplosiveInput)
    pressure: NflQuarterbackPressureInput = Field(default_factory=NflQuarterbackPressureInput)
    decision: NflQuarterbackDecisionInput = Field(default_factory=NflQuarterbackDecisionInput)
    mobility: NflQuarterbackMobilityInput = Field(default_factory=NflQuarterbackMobilityInput)
    situational: NflQuarterbackSituationalInput = Field(default_factory=NflQuarterbackSituationalInput)
    matchup: NflQuarterbackMatchupInput = Field(default_factory=NflQuarterbackMatchupInput)


class NflQuarterbackIntelligenceOutput(BaseModel):
    passing_efficiency_score: float
    explosive_passing_score: float
    pressure_resilience_score: float
    decision_quality_score: float
    mobility_score: float
    situational_score: float
    matchup_score: float
    ceiling_score: float
    floor_score: float
    volatility_score: float
    final_qb_score: float
    confidence: float
    warnings: list[str] = Field(default_factory=list)
    explainability: dict[str, float] = Field(default_factory=dict)
