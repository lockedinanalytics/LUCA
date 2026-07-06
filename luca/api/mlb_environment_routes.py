from __future__ import annotations

from fastapi import APIRouter

from luca.intelligence.mlb.context.game_context import score_game_context
from luca.intelligence.mlb.context.travel import score_travel_context
from luca.intelligence.mlb.context.umpire import score_umpire_profile
from luca.intelligence.mlb.environment.engine import calculate_environment_context
from luca.intelligence.mlb.environment.models import (
    EnvironmentContextInput,
    GameContextInput,
    ParkPhysicsInput,
    TravelContextInput,
    UmpireProfileInput,
    WeatherVectorInput,
)
from luca.intelligence.mlb.environment.park import score_park_physics
from luca.intelligence.mlb.environment.weather import score_weather_vector

router = APIRouter(prefix="/intelligence/mlb/environment", tags=["mlb-environment"])


@router.get("/weather/sample")
async def weather_sample():
    return score_weather_vector(WeatherVectorInput(
        temperature_f=86,
        humidity_pct=62,
        wind_speed_mph=13,
        wind_direction_degrees=45,
        barometric_pressure_inhg=29.82,
        precipitation_probability=10,
        roof_state="open",
        field_orientation_degrees=45,
    )).model_dump()


@router.get("/park/sample")
async def park_sample():
    return score_park_physics(ParkPhysicsInput(
        park_factor_runs=1.04,
        park_factor_hr=1.08,
        altitude_ft=522,
        foul_territory_score=48,
        wall_carry_score=56,
        surface_speed_score=52,
    )).model_dump()


@router.get("/travel/sample")
async def travel_sample():
    return score_travel_context(TravelContextInput(
        miles_traveled_last_3_days=1200,
        time_zone_shift=2,
        consecutive_road_games=5,
        rest_days=0,
        getaway_game=True,
        doubleheader=False,
        bullpen_travel_load_score=48,
    )).model_dump()


@router.get("/umpire/sample")
async def umpire_sample():
    return score_umpire_profile(UmpireProfileInput(
        name="Sample Umpire",
        strike_zone_score=56,
        pitcher_friendly_score=55,
        over_under_tendency_score=48,
        walk_rate_score=47,
        strikeout_rate_score=57,
        home_road_bias_score=51,
        consistency_score=60,
    )).model_dump()


@router.get("/context/sample")
async def context_sample():
    return score_game_context(GameContextInput(
        series_game_number=3,
        day_game_after_night=True,
        rubber_game=True,
        elimination_or_clinch_context=False,
        lineup_rest_risk_score=52,
        motivation_score=56,
        managerial_aggression_score=55,
    )).model_dump()


@router.get("/environment-v2/sample")
async def environment_v2_sample():
    return calculate_environment_context(EnvironmentContextInput(
        weather=WeatherVectorInput(temperature_f=86, humidity_pct=62, wind_speed_mph=13, wind_direction_degrees=45, barometric_pressure_inhg=29.82, precipitation_probability=10),
        park=ParkPhysicsInput(park_factor_runs=1.04, park_factor_hr=1.08, altitude_ft=522, foul_territory_score=48, wall_carry_score=56, surface_speed_score=52),
        travel=TravelContextInput(miles_traveled_last_3_days=1200, time_zone_shift=2, consecutive_road_games=5, rest_days=0, getaway_game=True, bullpen_travel_load_score=48),
        umpire=UmpireProfileInput(name="Sample Umpire", strike_zone_score=56, pitcher_friendly_score=55, over_under_tendency_score=48, walk_rate_score=47, strikeout_rate_score=57, consistency_score=60),
        game_context=GameContextInput(series_game_number=3, day_game_after_night=True, rubber_game=True, lineup_rest_risk_score=52, motivation_score=56, managerial_aggression_score=55),
    )).model_dump()
