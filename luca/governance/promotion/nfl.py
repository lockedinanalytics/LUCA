from __future__ import annotations

from luca.governance.promotion.models import PromotionRecord
from luca.validation.nfl.models import NflPromotionGateInput, NflPromotionGateOutput


def evaluate_nfl_promotion_gate(row: NflPromotionGateInput) -> NflPromotionGateOutput:
    failed = []
    warnings = list(row.validation.warnings)

    if row.validation.graded_decisions < row.min_decisions:
        failed.append("insufficient_sample")
    if row.validation.calibration_bias is not None and abs(row.validation.calibration_bias) > row.max_abs_calibration_bias:
        failed.append("calibration_bias")
    if row.validation.clv_health_score < row.min_clv_health_score:
        failed.append("clv_health")
    if row.validation.readiness_score < row.min_readiness_score:
        failed.append("readiness_score")

    for market in row.validation.market_slices:
        if market.roi is not None and market.roi < row.min_roi and market.decisions >= 30:
            failed.append(f"market_roi:{market.market}")

    approved = len(failed) == 0
    return NflPromotionGateOutput(
        approved=approved,
        readiness_score=row.validation.readiness_score,
        failed_gates=failed,
        warnings=warnings,
    )


def build_nfl_promotion_record(promotion_id: str, from_version: str, to_version: str, gate: NflPromotionGateOutput) -> PromotionRecord:
    return PromotionRecord(
        promotion_id=promotion_id,
        sport="nfl",
        from_version=from_version,
        to_version=to_version,
        approved=gate.approved,
        readiness_score=gate.readiness_score,
        failed_gates=gate.failed_gates,
        notes=gate.warnings,
    )
