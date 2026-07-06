from luca.core.models import Sport, TeamGame
from luca.features.mappers.mlb import MlbFeatureMapper
from luca.intelligence.mlb.context.game_context import score_game_context
from luca.intelligence.mlb.context.travel import score_travel_context
from luca.intelligence.mlb.context.umpire import score_umpire_profile
from luca.intelligence.mlb.environment.engine import calculate_environment_context
from luca.intelligence.mlb.environment.models import EnvironmentContextInput, GameContextInput, ParkPhysicsInput, TravelContextInput, UmpireProfileInput, WeatherVectorInput
from luca.intelligence.mlb.environment.park import score_park_physics
from luca.intelligence.mlb.environment.weather import score_weather_vector


def test_weather_vector_bounds():
    result = score_weather_vector(WeatherVectorInput(temperature_f=86, humidity_pct=62, wind_speed_mph=13, wind_direction_degrees=45))
    assert 0 <= result.carry_score <= 100
    assert result.wind_run_multiplier > 0


def test_park_physics_bounds():
    result = score_park_physics(ParkPhysicsInput(park_factor_runs=1.04, park_factor_hr=1.08, altitude_ft=522))
    assert 0 <= result.final_park_score <= 100


def test_travel_context_bounds():
    result = score_travel_context(TravelContextInput(miles_traveled_last_3_days=1200, time_zone_shift=2, consecutive_road_games=5))
    assert 0 <= result.travel_context_score <= 100


def test_umpire_profile_bounds():
    result = score_umpire_profile(UmpireProfileInput(name="U", strike_zone_score=56, pitcher_friendly_score=55, consistency_score=60))
    assert 0 <= result.final_umpire_score <= 100


def test_game_context_bounds():
    result = score_game_context(GameContextInput(series_game_number=3, day_game_after_night=True, rubber_game=True))
    assert 0 <= result.final_context_score <= 100


def test_environment_context_output():
    result = calculate_environment_context(EnvironmentContextInput(
        weather=WeatherVectorInput(temperature_f=86, humidity_pct=62, wind_speed_mph=13, wind_direction_degrees=45),
        park=ParkPhysicsInput(park_factor_runs=1.04, park_factor_hr=1.08, altitude_ft=522),
        travel=TravelContextInput(miles_traveled_last_3_days=1200, time_zone_shift=2),
        umpire=UmpireProfileInput(name="U", strike_zone_score=56, pitcher_friendly_score=55, consistency_score=60),
        game_context=GameContextInput(series_game_number=3),
    ))
    assert 0 <= result.final_environment_score <= 100
    assert "wind_run_multiplier" in result.explainability


def test_mapper_accepts_environment_context_v2():
    game = TeamGame(game_id="g1", sport=Sport.MLB, league="MLB", date="2026-07-04", away_team="Away", home_team="Home")
    modules = MlbFeatureMapper().build_modules(game, [], context={
        "environment_context_v2": {
            "weather": {"temperature_f": 86, "humidity_pct": 62, "wind_speed_mph": 13, "wind_direction_degrees": 45},
            "park": {"park_factor_runs": 1.04, "park_factor_hr": 1.08, "altitude_ft": 522},
            "travel": {"miles_traveled_last_3_days": 1200, "time_zone_shift": 2},
            "umpire": {"name": "U", "strike_zone_score": 56, "pitcher_friendly_score": 55, "consistency_score": 60},
            "game_context": {"series_game_number": 3}
        }
    })
    assert "wrm" in modules
    assert "environment" in modules
