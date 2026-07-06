from __future__ import annotations

from collections import defaultdict

from luca.validation.calibration.models import CalibrationBucket, CalibrationReport
from luca.validation.replay.models import HistoricalDecision


def _bucket(confidence: float, width: int = 5) -> str:
    low = int(confidence // width) * width
    high = low + width
    return f"{low}-{high}"


def build_calibration_report(decisions: list[HistoricalDecision], width: int = 5) -> CalibrationReport:
    graded = [d for d in decisions if d.result in {"win", "loss"}]
    grouped = defaultdict(list)
    for decision in graded:
        grouped[_bucket(decision.confidence, width)].append(decision)

    buckets: list[CalibrationBucket] = []
    brier_values: list[float] = []
    biases: list[float] = []

    for bucket_name, rows in sorted(grouped.items()):
        avg_conf = sum(d.confidence for d in rows) / len(rows)
        expected = avg_conf / 100.0
        actual = sum(d.result == "win" for d in rows) / len(rows)
        bias = actual - expected
        brier = sum(((d.confidence / 100.0) - (1.0 if d.result == "win" else 0.0)) ** 2 for d in rows) / len(rows)
        brier_values.append(brier)
        biases.append(bias)
        buckets.append(CalibrationBucket(
            bucket=bucket_name,
            decisions=len(rows),
            avg_confidence=round(avg_conf, 3),
            actual_win_rate=round(actual, 5),
            expected_win_rate=round(expected, 5),
            bias=round(bias, 5),
            brier_score=round(brier, 5),
        ))

    warnings = []
    if len(graded) < 30:
        warnings.append("Calibration sample is small; use caution.")
    if biases and abs(sum(biases) / len(biases)) >= 0.08:
        warnings.append("Material calibration bias detected.")

    overall_brier = sum(brier_values) / len(brier_values) if brier_values else None
    overall_bias = sum(biases) / len(biases) if biases else None

    return CalibrationReport(
        decisions=len(decisions),
        graded_decisions=len(graded),
        buckets=buckets,
        overall_brier_score=round(overall_brier, 5) if overall_brier is not None else None,
        calibration_bias=round(overall_bias, 5) if overall_bias is not None else None,
        warnings=warnings,
    )
