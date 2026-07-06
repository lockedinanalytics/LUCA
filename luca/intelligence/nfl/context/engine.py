from __future__ import annotations

from luca.intelligence.nfl.context.coaching import score_nfl_coaching
from luca.intelligence.nfl.context.environment import score_nfl_environment
from luca.intelligence.nfl.context.models import NflContextInput, NflContextOutput
from luca.intelligence.nfl.context.situational import score_nfl_situational
from luca.intelligence.nfl.context.special_teams import score_nfl_special_teams


def calculate_nfl_context(row: NflContextInput) -> NflContextOutput:
    situational = score_nfl_situational(row.situational)
    coaching = score_nfl_coaching(row.coaching)
    special = score_nfl_special_teams(row.special_teams)
    environment = score_nfl_environment(row.environment)

    warnings = []
    warnings.extend(situational.warnings)
    warnings.extend(coaching.warnings)
    warnings.extend(special.warnings)
    warnings.extend(environment.warnings)

    game_script = situational.pace_script_score * 0.38 + coaching.adjustment_score * 0.24 + environment.rushing_environment_score * 0.18 + special.field_position_score * 0.20
    pace = row.situational.pace_tendency_score * 0.55 + game_script * 0.25 + coaching.aggressiveness_score * 0.20
    hidden_yardage = special.final_special_teams_score * 0.62 + situational.travel_score * 0.18 + environment.kicking_environment_score * 0.20
    late_game = coaching.late_game_management_score * 0.60 + special.kicking_score * 0.24 + situational.motivation_score * 0.16

    final = (
        situational.final_situational_score * 0.26
        + coaching.final_coaching_score * 0.25
        + special.final_special_teams_score * 0.20
        + environment.final_environment_score * 0.20
        + late_game * 0.09
    )

    populated = 0
    total = 0
    for section in [row.situational, row.coaching, row.special_teams, row.environment]:
        data = section.model_dump()
        total += len(data)
        populated += sum(v is not None for v in data.values())
    confidence = 45 + min(45, populated / max(1, total) * 45)
    if warnings:
        confidence -= min(12, len(warnings))

    explainability = {
        "situational": situational.final_situational_score,
        "coaching": coaching.final_coaching_score,
        "special_teams": special.final_special_teams_score,
        "environment": environment.final_environment_score,
        "game_script": round(game_script, 2),
        "pace": round(pace, 2),
        "hidden_yardage": round(hidden_yardage, 2),
        "late_game": round(late_game, 2),
    }

    return NflContextOutput(
        situational_score=situational.final_situational_score,
        coaching_score=coaching.final_coaching_score,
        special_teams_score=special.final_special_teams_score,
        environment_score=environment.final_environment_score,
        game_script_projection=round(max(0, min(100, game_script)), 2),
        pace_projection=round(max(0, min(100, pace)), 2),
        weather_risk=environment.weather_risk_score,
        hidden_yardage_edge=round(max(0, min(100, hidden_yardage)), 2),
        late_game_management_edge=round(max(0, min(100, late_game)), 2),
        final_context_score=round(max(0, min(100, final)), 2),
        confidence=round(max(0, min(100, confidence)), 2),
        warnings=warnings,
        explainability=explainability,
    )
