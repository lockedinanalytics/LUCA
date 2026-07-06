from __future__ import annotations

from pydantic import BaseModel


class CalibrationBucket(BaseModel):
    bucket: str
    decisions: int
    avg_confidence: float
    actual_win_rate: float | None
    expected_win_rate: float
    bias: float | None
    brier_score: float | None


class CalibrationReport(BaseModel):
    decisions: int
    graded_decisions: int
    buckets: list[CalibrationBucket]
    overall_brier_score: float | None
    calibration_bias: float | None
    warnings: list[str]
