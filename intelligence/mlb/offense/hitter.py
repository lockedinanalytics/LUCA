from __future__ import annotations

from luca.intelligence.mlb.offense.models import HitterInput, HitterQualityOutput


def score_hitter(row: HitterInput) -> HitterQualityOutput:
    warnings: list[str] = []

    on_base = (
        row.xwoba_score * 0.38
        + row.contact_score * 0.20
        + row.chase_discipline_score * 0.16
        + row.walk_score * 0.16
        + row.recent_form_score * 0.10
    )

    damage = (
        row.xslg_score * 0.34
        + row.hard_hit_score * 0.24
        + row.barrel_score * 0.24
        + row.pitch_type_fit_score * 0.10
        + row.recent_form_score * 0.08
    )

    discipline = (
        row.chase_discipline_score * 0.35
        + row.strikeout_avoidance_score * 0.35
        + row.walk_score * 0.20
        + row.contact_score * 0.10
    )

    matchup = (
        row.platoon_score * 0.40
        + row.pitch_type_fit_score * 0.35
        + row.recent_form_score * 0.15
        + row.baserunning_score * 0.10
    )

    spot_multiplier = 1.0
    if row.lineup_spot <= 4:
        spot_multiplier = 1.04
    elif row.lineup_spot >= 8:
        spot_multiplier = 0.96

    final = (
        on_base * 0.30
        + damage * 0.28
        + discipline * 0.18
        + matchup * 0.18
        + row.baserunning_score * 0.06
    ) * spot_multiplier - row.injury_penalty

    if row.injury_penalty >= 5:
        warnings.append(f"{row.name}: injury/availability penalty applied.")
    if row.strikeout_avoidance_score < 42:
        warnings.append(f"{row.name}: elevated strikeout risk.")
    if row.platoon_score < 42:
        warnings.append(f"{row.name}: platoon disadvantage.")

    return HitterQualityOutput(
        name=row.name,
        lineup_spot=row.lineup_spot,
        on_base_score=round(max(0, min(100, on_base)), 2),
        damage_score=round(max(0, min(100, damage)), 2),
        discipline_score=round(max(0, min(100, discipline)), 2),
        matchup_score=round(max(0, min(100, matchup)), 2),
        final_hitter_score=round(max(0, min(100, final)), 2),
        warnings=warnings,
    )
