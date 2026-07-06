from __future__ import annotations

from pydantic import BaseModel


class DriftMetric(BaseModel):
    feature: str
    baseline_mean: float
    current_mean: float
    delta: float
    drift_score: float
    status: str


class DriftReport(BaseModel):
    metrics: list[DriftMetric]
    warnings: list[str]
