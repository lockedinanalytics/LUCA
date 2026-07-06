from __future__ import annotations

from collections import defaultdict

from luca.validation.attribution.models import FeatureAttributionReport, FeatureAttributionRow
from luca.validation.replay.models import HistoricalDecision


def build_feature_attribution(decisions: list[HistoricalDecision]) -> FeatureAttributionReport:
    graded = [d for d in decisions if d.result in {"win", "loss"}]
    values = defaultdict(lambda: {"win": [], "loss": []})

    for decision in graded:
        for feature, score in decision.module_snapshot.items():
            try:
                values[feature][decision.result].append(float(score))
            except (TypeError, ValueError):
                continue

    rows: list[FeatureAttributionRow] = []
    for feature, groups in sorted(values.items()):
        wins = groups["win"]
        losses = groups["loss"]
        avg_win = sum(wins) / len(wins) if wins else None
        avg_loss = sum(losses) / len(losses) if losses else None
        spread = (avg_win - avg_loss) if avg_win is not None and avg_loss is not None else None

        if spread is None:
            signal = "insufficient"
        elif spread >= 4:
            signal = "positive"
        elif spread <= -4:
            signal = "negative"
        else:
            signal = "neutral"

        rows.append(FeatureAttributionRow(
            feature=feature,
            decisions=len(wins) + len(losses),
            avg_score_wins=round(avg_win, 3) if avg_win is not None else None,
            avg_score_losses=round(avg_loss, 3) if avg_loss is not None else None,
            spread=round(spread, 3) if spread is not None else None,
            contribution_signal=signal,
        ))

    warnings = []
    if len(graded) < 30:
        warnings.append("Attribution sample is small; signals are directional only.")

    return FeatureAttributionReport(rows=rows, warnings=warnings)
