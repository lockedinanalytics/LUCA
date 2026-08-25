from __future__ import annotations

from pydantic import BaseModel, Field

from luca.core.math_utils import clamp


class SurvivorTeamOption(BaseModel):
    team: str
    win_probability: float = Field(ge=0.0, le=1.0)
    future_value: float = Field(ge=0.0, le=100.0)
    ownership_projection: float = Field(ge=0.0, le=100.0)
    scarcity_score: float = Field(ge=0.0, le=100.0)
    schedule_path_value: float = Field(ge=0.0, le=100.0)
    risk_stability: float = Field(ge=0.0, le=100.0)


class SurvivorPickResult(BaseModel):
    team: str
    survivor_score: float
    pick_class: str
    notes: list[str]


def score_survivor_option(option: SurvivorTeamOption) -> float:
    score = (
        option.win_probability * 100 * 0.35
        + option.future_value * 0.20
        + (100 - option.ownership_projection) * 0.15
        + option.scarcity_score * 0.12
        + option.schedule_path_value * 0.10
        + option.risk_stability * 0.08
    )
    return clamp(score)


def classify_survivor_pick(score: float, win_probability: float) -> str:
    if win_probability < 0.65:
        return "avoid"
    if score >= 85:
        return "balanced_elite"
    if score >= 78:
        return "balanced"
    if score >= 70:
        return "leverage"
    return "safe_only"


def rank_survivor_options(options: list[SurvivorTeamOption]) -> list[SurvivorPickResult]:
    results = []
    for option in options:
        score = score_survivor_option(option)
        results.append(SurvivorPickResult(
            team=option.team,
            survivor_score=round(score, 2),
            pick_class=classify_survivor_pick(score, option.win_probability),
            notes=["Uses weekly survival + future value + ownership leverage."],
        ))
    return sorted(results, key=lambda row: row.survivor_score, reverse=True)
