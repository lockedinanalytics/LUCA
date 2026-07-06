from __future__ import annotations

from pydantic import BaseModel

from luca.core.math_utils import clamp, weighted_average


class EvidenceInput(BaseModel):
    module_scores: dict[str, float]
    module_weights: dict[str, float]
    market_edge_score: float = 50.0
    simulation_score: float = 50.0
    calibration_score: float = 50.0
    risk_penalty: float = 0.0


class EvidenceFusionResult(BaseModel):
    fused_score: float
    top_positive_drivers: list[str]
    top_negative_drivers: list[str]
    notes: list[str]


def fuse_evidence(row: EvidenceInput) -> EvidenceFusionResult:
    base = weighted_average(row.module_scores, row.module_weights)
    fused = (
        base * 0.55
        + row.market_edge_score * 0.15
        + row.simulation_score * 0.15
        + row.calibration_score * 0.10
        + 50.0 * 0.05
        - row.risk_penalty
    )

    ordered = sorted(row.module_scores.items(), key=lambda item: item[1], reverse=True)
    positives = [key for key, value in ordered[:5] if value >= 55]
    negatives = [key for key, value in ordered[-5:] if value <= 48]

    return EvidenceFusionResult(
        fused_score=round(clamp(fused), 2),
        top_positive_drivers=positives,
        top_negative_drivers=negatives,
        notes=["Evidence fused from modules, market, simulation, calibration, and risk penalty."],
    )
