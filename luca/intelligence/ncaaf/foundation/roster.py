from __future__ import annotations

from luca.intelligence.ncaaf.foundation.models import RecruitingProfileInput, ReturningProductionInput, TransferPortalInput


def score_recruiting_profile(row: RecruitingProfileInput) -> tuple[float, list[str]]:
    warnings: list[str] = []
    score = row.recruiting_composite_score * 0.38 + row.recruiting_momentum_score * 0.22 + row.position_group_depth_score * 0.22 + 50.0 * 0.18
    score += min(15, row.blue_chip_ratio * 20)
    if row.avg_star_rating is not None:
        score += (row.avg_star_rating - 3.0) * 8.0
    if row.blue_chip_ratio >= 0.50:
        warnings.append("Blue-chip ratio indicates high-end talent profile.")
    if row.position_group_depth_score < 42:
        warnings.append("Position-group depth is thin.")
    return round(max(0, min(100, score)), 2), warnings


def score_returning_production(row: ReturningProductionInput) -> tuple[float, list[str]]:
    warnings: list[str] = []
    offense = row.offensive_returning_production_pct * 0.45 + row.returning_starters_offense * 3.0 + row.returning_qb_experience_score * 0.25 + row.offensive_line_continuity_score * 0.20
    defense = row.defensive_returning_production_pct * 0.55 + row.returning_starters_defense * 3.2
    score = offense * 0.52 + defense * 0.48
    if row.returning_qb_experience_score < 42:
        warnings.append("Returning QB experience risk.")
    if row.offensive_line_continuity_score < 42:
        warnings.append("Offensive line continuity risk.")
    return round(max(0, min(100, score)), 2), warnings


def score_transfer_portal(row: TransferPortalInput) -> tuple[float, list[str]]:
    warnings: list[str] = []
    score = (
        row.transfer_gain_score * 0.30
        + (100 - row.transfer_loss_score) * 0.20
        + row.quarterback_transfer_score * 0.20
        + row.defensive_transfer_score * 0.14
        + (100 - row.portal_volatility_score) * 0.16
    )
    if row.portal_volatility_score >= 65:
        warnings.append("Portal volatility can reduce early-season reliability.")
    if row.quarterback_transfer_score >= 62:
        warnings.append("Quarterback transfer profile improves ceiling.")
    return round(max(0, min(100, score)), 2), warnings
