from luca.core.models import Sport, TeamGame
from luca.features.mappers.nfl.mapper import NflFeatureMapper
from luca.intelligence.nfl.context.engine import calculate_nfl_context
from luca.intelligence.nfl.context.models import NflContextInput, NflEnvironmentInput, NflSituationalInput


def test_nfl_context_bounds():
    result = calculate_nfl_context(NflContextInput(
        situational=NflSituationalInput(rest_days=7, opponent_rest_days=6, miles_traveled=900, time_zone_shift=1),
        environment=NflEnvironmentInput(wind_mph=12, temperature_f=42, roof_state="open"),
    ))
    assert 0 <= result.final_context_score <= 100
    assert result.confidence > 0


def test_nfl_mapper_accepts_context_v2():
    game = TeamGame(game_id="g1", sport=Sport.NFL, league="NFL", date="2026-09-01", away_team="Away", home_team="Home")
    modules = NflFeatureMapper().build_modules(game, [], context={
        "context_v2": {
            "situational": {"rest_days": 7, "opponent_rest_days": 6, "miles_traveled": 900, "time_zone_shift": 1},
            "environment": {"wind_mph": 12, "temperature_f": 42, "roof_state": "open"},
        }
    })
    assert "context_edge" in modules
    assert "special_teams_edge" in modules
