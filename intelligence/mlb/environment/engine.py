from __future__ import annotations

from luca.intelligence.mlb.context.game_context import score_game_context
from luca.intelligence.mlb.context.travel import score_travel_context
from luca.intelligence.mlb.context.umpire import score_umpire_profile
from luca.intelligence.mlb.environment.models import EnvironmentContextInput, EnvironmentContextOutput
from luca.intelligence.mlb.environment.park import score_park_physics
from luca.intelligence.mlb.environment.weather import score_weather_vector


def calculate_environment_context(row: EnvironmentContextInput) -> EnvironmentContextOutput:
    weather = score_weather_vector(row.weather)
    park = score_park_physics(row.park)
    travel = score_travel_context(row.travel)
    umpire = score_umpire_profile(row.umpire)
    game = score_game_context(row.game_context)

    warnings = []
    for block in [weather, park, travel, umpire, game]:
        warnings.extend(block.warnings)

    run_modifier = (
        (weather.carry_score - 50) * 0.006
        + (weather.wind_out_score - 50) * 0.007
        + (park.final_park_score - 50) * 0.006
        + (umpire.run_environment_score - 50) * 0.004
    )

    pitching_modifier = (
        (umpire.pitcher_support_score - 50) * 0.006
        + (100 - weather.volatility_score - 50) * 0.003
        + (travel.travel_context_score - 50) * 0.002
    )

    offensive_modifier = (
        run_modifier
        + (game.final_context_score - 50) * 0.003
        + (travel.travel_context_score - 50) * 0.002
    )

    final = (
        weather.carry_score * 0.18
        + park.final_park_score * 0.22
        + travel.travel_context_score * 0.16
        + umpire.final_umpire_score * 0.18
        + game.final_context_score * 0.16
        + 50 * 0.10
    )

    populated = 0
    total = 0
    for section in [row.weather, row.park, row.travel, row.umpire, row.game_context]:
        data = section.model_dump()
        total += len(data)
        populated += sum(value is not None for value in data.values())
    confidence = 45 + (populated / total) * 45 if total else 45

    explainability = {
        "weather": round(weather.carry_score, 2),
        "park": park.final_park_score,
        "travel": travel.travel_context_score,
        "umpire": umpire.final_umpire_score,
        "game_context": game.final_context_score,
        "wind_run_multiplier": weather.wind_run_multiplier,
        "weather_total_adjustment": weather.total_adjustment,
    }

    return EnvironmentContextOutput(
        weather_score=round(weather.carry_score, 2),
        park_score=park.final_park_score,
        travel_score=travel.travel_context_score,
        umpire_score=umpire.final_umpire_score,
        context_score=game.final_context_score,
        run_environment_modifier=round(run_modifier, 4),
        pitching_environment_modifier=round(pitching_modifier, 4),
        offensive_environment_modifier=round(offensive_modifier, 4),
        final_environment_score=round(max(0, min(100, final)), 2),
        confidence=round(max(0, min(100, confidence)), 2),
        warnings=warnings,
        explainability=explainability,
    )
