from __future__ import annotations

from luca.intelligence.mlb.offense.models import PlatoonInput, PlatoonOutput


PLATOON_ENGINE_VERSION = "platoon_governance_diagnostic_cleanup"


def _clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, float(value)))


def score_platoon_fit(row: PlatoonInput) -> PlatoonOutput:
    """
    Score platoon fit for upstream offensive intelligence.

    Governance migration note:
    Platoon scoring is diagnostic only. It does not select plays, certify
    Presidential eligibility, apply Governance penalties, rank wagers, or
    assign units.
    """
    warnings: list[str] = []

    total_pa = (
        row.projected_lhp_plate_appearances
        + row.projected_rhp_plate_appearances
    )

    if total_pa <= 0:
        starter = row.lineup_platoon_score
        warnings.append(
            "No projected handedness plate appearance split supplied; using baseline lineup platoon score."
        )
    else:
        imbalance = abs(
            row.projected_lhp_plate_appearances
            - row.projected_rhp_plate_appearances
        ) / total_pa

        starter_adjustment = imbalance * 4.0
        if row.lineup_platoon_score < 50.0:
            starter_adjustment *= -1.0

        starter = row.lineup_platoon_score + starter_adjustment

    bullpen = row.opposing_bullpen_hand_balance_score
    flexibility = (
        row.switch_hitter_flex_score * 0.65
        + row.lineup_platoon_score * 0.35
    )

    if row.lineup_platoon_score < 44.0:
        warnings.append("Projected lineup has platoon disadvantage.")

    if row.switch_hitter_flex_score >= 60.0:
        warnings.append(
            "Switch-hitter flexibility improves late-game matchup stability."
        )

    final = starter * 0.45 + bullpen * 0.25 + flexibility * 0.30

    return PlatoonOutput(
        starter_platoon_score=round(_clamp(starter), 2),
        bullpen_platoon_score=round(_clamp(bullpen), 2),
        flexibility_score=round(_clamp(flexibility), 2),
        final_platoon_score=round(_clamp(final), 2),
        warnings=warnings,
    )
