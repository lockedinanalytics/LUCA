from __future__ import annotations

from pydantic import BaseModel, Field


class NflSituationalInput(BaseModel):
    rest_days: int | None = None
    opponent_rest_days: int | None = None
    short_week: bool = False
    off_bye: bool = False
    opponent_off_bye: bool = False
    international_travel: bool = False
    miles_traveled: float = 0.0
    time_zone_shift: int = 0
    divisional_game: bool = False
    revenge_spot_score: float = 50.0
    lookahead_risk_score: float = 50.0
    pace_tendency_score: float = 50.0
    game_script_stability_score: float = 50.0


class NflSituationalOutput(BaseModel):
    rest_edge_score: float
    travel_score: float
    motivation_score: float
    pace_script_score: float
    final_situational_score: float
    warnings: list[str] = Field(default_factory=list)


class NflCoachingInput(BaseModel):
    fourth_down_aggression_score: float = 50.0
    two_point_strategy_score: float = 50.0
    red_zone_play_call_score: float = 50.0
    run_pass_adaptability_score: float = 50.0
    clock_management_score: float = 50.0
    challenge_efficiency_score: float = 50.0
    halftime_adjustment_score: float = 50.0
    coordinator_matchup_score: float = 50.0
    personnel_grouping_edge_score: float = 50.0


class NflCoachingOutput(BaseModel):
    aggressiveness_score: float
    late_game_management_score: float
    red_zone_management_score: float
    adjustment_score: float
    final_coaching_score: float
    warnings: list[str] = Field(default_factory=list)


class NflSpecialTeamsInput(BaseModel):
    kicker_consistency_score: float = 50.0
    long_fg_score: float = 50.0
    weather_adjusted_kicking_score: float = 50.0
    punter_field_position_score: float = 50.0
    kickoff_return_score: float = 50.0
    punt_return_score: float = 50.0
    coverage_unit_score: float = 50.0
    block_pressure_score: float = 50.0
    hidden_yardage_score: float = 50.0


class NflSpecialTeamsOutput(BaseModel):
    kicking_score: float
    field_position_score: float
    return_game_score: float
    coverage_pressure_score: float
    final_special_teams_score: float
    warnings: list[str] = Field(default_factory=list)


class NflEnvironmentInput(BaseModel):
    wind_mph: float | None = None
    precipitation_score: float = 50.0
    snow_score: float = 50.0
    temperature_f: float | None = None
    humidity_pct: float | None = None
    elevation_ft: float = 0.0
    roof_state: str = "open"
    surface_score: float = 50.0
    weather_severity_score: float = 50.0


class NflEnvironmentOutput(BaseModel):
    passing_environment_score: float
    rushing_environment_score: float
    kicking_environment_score: float
    weather_risk_score: float
    final_environment_score: float
    warnings: list[str] = Field(default_factory=list)


class NflContextInput(BaseModel):
    situational: NflSituationalInput = Field(default_factory=NflSituationalInput)
    coaching: NflCoachingInput = Field(default_factory=NflCoachingInput)
    special_teams: NflSpecialTeamsInput = Field(default_factory=NflSpecialTeamsInput)
    environment: NflEnvironmentInput = Field(default_factory=NflEnvironmentInput)


class NflContextOutput(BaseModel):
    situational_score: float
    coaching_score: float
    special_teams_score: float
    environment_score: float
    game_script_projection: float
    pace_projection: float
    weather_risk: float
    hidden_yardage_edge: float
    late_game_management_edge: float
    final_context_score: float
    confidence: float
    warnings: list[str] = Field(default_factory=list)
    explainability: dict[str, float] = Field(default_factory=dict)
