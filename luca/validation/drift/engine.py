from __future__ import annotations

from collections import defaultdict

from luca.validation.drift.models import DriftMetric, DriftReport
from luca.validation.replay.models import HistoricalDecision


def _means(decisions: list[HistoricalDecision]) -> dict[str, float]:
    values = defaultdict(list)
    for d in decisions:
        for key, value in d.module_snapshot.items():
            try:
                values[key].append(float(value))
            except (TypeError, ValueError):
                continue
    return {k: sum(v) / len(v) for k, v in values.items() if v}


def build_drift_report(baseline: list[HistoricalDecision], current: list[HistoricalDecision]) -> DriftReport:
    base = _means(baseline)
    cur = _means(current)
    metrics = []

    for feature in sorted(set(base) & set(cur)):
        delta = cur[feature] - base[feature]
        drift_score = min(100, abs(delta) * 5)
        if drift_score >= 35:
            status = "material"
        elif drift_score >= 18:
            status = "watch"
        else:
            status = "stable"
        metrics.append(DriftMetric(
            feature=feature,
            baseline_mean=round(base[feature], 3),
            current_mean=round(cur[feature], 3),
            delta=round(delta, 3),
            drift_score=round(drift_score, 3),
            status=status,
        ))

    warnings = [f"{m.feature} drift status: {m.status}" for m in metrics if m.status in {"watch", "material"}]
    return DriftReport(metrics=metrics, warnings=warnings)
