from __future__ import annotations

from pydantic import BaseModel

from luca.core.math_utils import clamp


class TeamProjection(BaseModel):
    team: str
    offensive_score: float = 50.0
    defensive_opponent_score: float = 50.0
    pace_score: float = 50.0
    environment_score: float = 50.0
    market_score: float = 50.0
    baseline_points: float = 0.0


def project_team_points(proj: TeamProjection) -> float:
    score = (
        proj.offensive_score * 0.35
        + (100 - proj.defensive_opponent_score) * 0.25
        + proj.pace_score * 0.15
        + proj.environment_score * 0.10
        + proj.market_score * 0.05
        + 50 * 0.10
    )
    modifier = (clamp(score) - 50.0) / 50.0
    return round(max(0.0, proj.baseline_points * (1 + modifier * 0.25)), 3)


def project_game_total(home: TeamProjection, away: TeamProjection) -> float:
    return round(project_team_points(home) + project_team_points(away), 3)


def project_game_margin(home: TeamProjection, away: TeamProjection) -> float:
    return round(project_team_points(home) - project_team_points(away), 3)
