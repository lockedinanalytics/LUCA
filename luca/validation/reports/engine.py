from __future__ import annotations

from pydantic import BaseModel

from luca.validation.attribution.engine import build_feature_attribution
from luca.validation.attribution.models import FeatureAttributionReport
from luca.validation.calibration.engine import build_calibration_report
from luca.validation.calibration.models import CalibrationReport
from luca.validation.performance.engine import build_performance_report
from luca.validation.performance.models import PerformanceReport
from luca.validation.replay.engine import summarize_replay
from luca.validation.replay.models import ReplayBatch, ReplaySummary


class ValidationReport(BaseModel):
    replay: ReplaySummary
    calibration: CalibrationReport
    attribution: FeatureAttributionReport
    performance: PerformanceReport


def build_validation_report(batch: ReplayBatch) -> ValidationReport:
    return ValidationReport(
        replay=summarize_replay(batch),
        calibration=build_calibration_report(batch.decisions),
        attribution=build_feature_attribution(batch.decisions),
        performance=build_performance_report(batch.decisions),
    )
