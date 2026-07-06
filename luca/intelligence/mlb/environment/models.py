from __future__ import annotations

from pydantic import BaseModel, Field


class WeatherVectorInput(BaseModel):
    temperature_f: float | None = None
    humidity_pct: float | None = None
    wind_speed_mph: float | None = None
    wind_direction_degrees: float | None = None
    barometric_pressure_inhg: float | None = None
    precipitation_probability: float | None = None
    roof_state: str = "open"
    field_orientation_degrees: float = 45.0


class WeatherVectorOutput(BaseModel):
    carry_score: float
    wind_out_score: float
    suppression_score: float
    volatility_score: float
    wind_run_multiplier: float
    total_adjustment: float
    warnings: list[str] = Field(default_factory=list)


class ParkPhysicsInput(BaseModel):
    park_factor_runs: float = 1.0
    park_factor_hr: float = 1.0
    altitude_ft: float = 0.0
    foul_territory_score: float = 50.0
    wall_carry_score: float = 50.0
    surface_speed_score: float = 50.0
    roof_state: str = "open"


class ParkPhysicsOutput(BaseModel):
    run_factor_score: float
    power_factor_score: float
    batted_ball_carry_score: float
    park_suppression_score: float
    final_park_score: float
    warnings: list[str] = Field(default_factory=list)


class TravelContextInput(BaseModel):
    miles_traveled_last_3_days: float = 0.0
    time_zone_shift: int = 0
    consecutive_road_games: int = 0
    rest_days: int = 0
    getaway_game: bool = False
    doubleheader: bool = False
    bullpen_travel_load_score: float = 50.0


class TravelContextOutput(BaseModel):
    fatigue_score: float
    circadian_score: float
    schedule_pressure_score: float
    travel_context_score: float
    warnings: list[str] = Field(default_factory=list)


class UmpireProfileInput(BaseModel):
    name: str = "Unknown Umpire"
    strike_zone_score: float = 50.0
    pitcher_friendly_score: float = 50.0
    over_under_tendency_score: float = 50.0
    walk_rate_score: float = 50.0
    strikeout_rate_score: float = 50.0
    home_road_bias_score: float = 50.0
    consistency_score: float = 50.0


class UmpireProfileOutput(BaseModel):
    zone_score: float
    run_environment_score: float
    pitcher_support_score: float
    volatility_score: float
    final_umpire_score: float
    warnings: list[str] = Field(default_factory=list)


class GameContextInput(BaseModel):
    series_game_number: int | None = None
    day_game_after_night: bool = False
    rubber_game: bool = False
    elimination_or_clinch_context: bool = False
    lineup_rest_risk_score: float = 50.0
    motivation_score: float = 50.0
    managerial_aggression_score: float = 50.0


class GameContextOutput(BaseModel):
    rest_context_score: float
    motivation_context_score: float
    managerial_context_score: float
    final_context_score: float
    warnings: list[str] = Field(default_factory=list)


class EnvironmentContextInput(BaseModel):
    weather: WeatherVectorInput = Field(default_factory=WeatherVectorInput)
    park: ParkPhysicsInput = Field(default_factory=ParkPhysicsInput)
    travel: TravelContextInput = Field(default_factory=TravelContextInput)
    umpire: UmpireProfileInput = Field(default_factory=UmpireProfileInput)
    game_context: GameContextInput = Field(default_factory=GameContextInput)


class EnvironmentContextOutput(BaseModel):
    weather_score: float
    park_score: float
    travel_score: float
    umpire_score: float
    context_score: float
    run_environment_modifier: float
    pitching_environment_modifier: float
    offensive_environment_modifier: float
    final_environment_score: float
    confidence: float
    warnings: list[str] = Field(default_factory=list)
    explainability: dict[str, float] = Field(default_factory=dict)
