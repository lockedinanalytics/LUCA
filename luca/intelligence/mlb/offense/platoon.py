from __future__ import annotations

from luca.intelligence.mlb.offense.models import PlatoonInput, PlatoonOutput


def score_platoon_fit(row: PlatoonInput) -> PlatoonOutput:
    warnings: list[str] = []

    total_pa = row.projected_lhp_plate_appearances + row.projected_rhp_plate_appearances
    if total_pa <= 0:
        starter = row.lineup_platoon_score
    else:
        # Starter matchup receives more weight if one side dominates projected PA.
        imbalance = abs(row.projected_lhp_plate_appearances - row.projected_rhp_plate_appearances) / total_pa
        starter = row.lineup_platoon_score + (imbalance * 4 if row.lineup_platoon_score >= 50 else -imbalance * 4)

    bullpen = row.opposing_bullpen_hand_balance_score
    flexibility = row.switch_hitter_flex_score * 0.65 + row.lineup_platoon_score * 0.35

    if row.lineup_platoon_score < 44:
        warnings.append("Projected lineup has platoon disadvantage.")
    if row.switch_hitter_flex_score >= 60:
        warnings.append("Switch-hitter flexibility improves late-game matchup stability.")

    final = starter * 0.45 + bullpen * 0.25 + flexibility * 0.30

    return PlatoonOutput(
        starter_platoon_score=round(max(0, min(100, starter)), 2),
        bullpen_platoon_score=round(max(0, min(100, bullpen)), 2),
        flexibility_score=round(max(0, min(100, flexibility)), 2),
        final_platoon_score=round(max(0, min(100, final)), 2),
        warnings=warnings,
    )
