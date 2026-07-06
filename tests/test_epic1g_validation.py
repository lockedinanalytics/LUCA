from luca.validation.attribution.engine import build_feature_attribution
from luca.validation.calibration.engine import build_calibration_report
from luca.validation.drift.engine import build_drift_report
from luca.validation.performance.engine import build_performance_report
from luca.validation.replay.engine import summarize_replay
from luca.validation.replay.models import HistoricalDecision, ReplayBatch
from luca.validation.reports.engine import build_validation_report


def decisions():
    rows = []
    for i in range(1, 41):
        win = i % 3 != 0
        confidence = 58 + (i % 8) * 4
        rows.append(HistoricalDecision(
            decision_id=f"d{i}",
            date="2026-07-04",
            sport="mlb",
            league="MLB",
            game_id=f"g{i}",
            market="moneyline" if i % 2 else "total",
            category="presidential" if i % 10 == 0 else "cabinet",
            selection="Home",
            odds=-110,
            units=1.0,
            confidence=confidence,
            result="win" if win else "loss",
            units_won_lost=0.91 if win else -1.0,
            module_snapshot={"sp": 55 + (i % 7), "bsi": 54 + (i % 5), "rcp": 53 + (i % 6), "smi": 52 + (i % 8)},
        ))
    return rows


def test_replay_summary():
    summary = summarize_replay(ReplayBatch(replay_id="x", model_version="test", decisions=decisions()))
    assert summary.graded_decisions == 40
    assert summary.roi is not None


def test_calibration_report():
    report = build_calibration_report(decisions())
    assert report.graded_decisions == 40
    assert len(report.buckets) > 0


def test_feature_attribution():
    report = build_feature_attribution(decisions())
    assert len(report.rows) > 0


def test_performance_report():
    report = build_performance_report(decisions())
    assert len(report.by_category) > 0


def test_drift_report():
    baseline = decisions()[:20]
    current = decisions()[20:]
    for row in current:
        row.module_snapshot["smi"] += 8
    report = build_drift_report(baseline, current)
    assert len(report.metrics) > 0


def test_validation_report():
    report = build_validation_report(ReplayBatch(replay_id="x", model_version="test", decisions=decisions()))
    assert report.replay.decisions == 40
