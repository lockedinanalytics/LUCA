from __future__ import annotations
from luca.core.models import GovernanceStatus, PickCategory

def apply_governance(confidence: float, expected_value: float|None, risk_grade: str="medium", data_completeness: float=1.0, model_conflict: bool=False) -> GovernanceStatus:
    if data_completeness < .70 or model_conflict: return GovernanceStatus.HOLD
    if expected_value is None or expected_value <= 0: return GovernanceStatus.PASS
    if risk_grade.lower() in {"extreme","avoid"}: return GovernanceStatus.AVOID
    if confidence < 70: return GovernanceStatus.PASS
    return GovernanceStatus.APPROVED

def assign_category(luca_score: float, is_total: bool=False, is_prop: bool=False) -> PickCategory:
    if is_prop: return PickCategory.PROP
    if is_total: return PickCategory.BEST_TOTAL if luca_score >= 80 else PickCategory.SECONDARY_TOTAL
    if luca_score >= 90: return PickCategory.PRESIDENTIAL
    if luca_score >= 85: return PickCategory.VICE_PRESIDENTIAL
    if luca_score >= 80: return PickCategory.CABINET
    if luca_score >= 75: return PickCategory.LEAN
    return PickCategory.PASS
