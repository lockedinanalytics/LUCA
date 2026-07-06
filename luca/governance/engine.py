from __future__ import annotations

from luca.core.models import GovernanceStatus


def apply_governance(
    confidence: float,
    expected_value: float | None,
    risk_grade: str = "medium",
    data_completeness: float = 1.0,
) -> GovernanceStatus:
    """Universal LUCA governance gate."""
    if data_completeness < 0.70:
        return GovernanceStatus.HOLD
    if expected_value is None or expected_value <= 0:
        return GovernanceStatus.PASS
    if risk_grade.lower() in {"extreme", "avoid"}:
        return GovernanceStatus.AVOID
    if confidence < 70:
        return GovernanceStatus.PASS
    return GovernanceStatus.APPROVED


def category_from_score(score: float) -> str:
    if score >= 90:
        return "presidential_eligible"
    if score >= 85:
        return "vice_presidential_eligible"
    if score >= 80:
        return "cabinet_eligible"
    if score >= 75:
        return "lean"
    return "pass"
