from __future__ import annotations

from collections import defaultdict

from luca.core.math_utils import american_to_implied_probability
from luca.validation.calibration.engine import build_calibration_report
from luca.validation.nfl.models import NflMarketValidationSlice, NflReplayInput, NflValidationSummary


def _clv_delta(decision) -> float | None:
    if decision.odds is None or decision.closing_odds is None:
        return None
    return american_to_implied_probability(decision.closing_odds) - american_to_implied_probability(decision.odds)


def build_nfl_validation_summary(row: NflReplayInput) -> NflValidationSummary:
    grouped = defaultdict(list)
    graded = [d for d in row.decisions if d.result in {"win", "loss", "push"}]
    for decision in graded:
        grouped[decision.market].append(decision)

    slices: list[NflMarketValidationSlice] = []
    clv_values = []
    briers = []

    for market, decisions in sorted(grouped.items()):
        wins = sum(d.result == "win" for d in decisions)
        losses = sum(d.result == "loss" for d in decisions)
        pushes = sum(d.result == "push" for d in decisions)
        units = round(sum(float(d.units_won_lost or 0.0) for d in decisions), 4)
        risked = sum(float(d.units or 0.0) for d in decisions)
        roi = round(units / risked, 5) if risked > 0 else None

        market_clv = [_clv_delta(d) for d in decisions]
        market_clv = [v for v in market_clv if v is not None]
        clv_values.extend(market_clv)
        avg_clv = round(sum(market_clv) / len(market_clv), 5) if market_clv else None

        graded_binary = [d for d in decisions if d.result in {"win", "loss"} and d.projected_probability is not None]
        if graded_binary:
            brier = sum((float(d.projected_probability) - (1.0 if d.result == "win" else 0.0)) ** 2 for d in graded_binary) / len(graded_binary)
            briers.append(brier)
        else:
            brier = None

        slices.append(NflMarketValidationSlice(
            market=market,
            decisions=len(decisions),
            wins=wins,
            losses=losses,
            pushes=pushes,
            units=units,
            roi=roi,
            avg_clv_delta=avg_clv,
            brier_score=round(brier, 5) if brier is not None else None,
        ))

    calibration = build_calibration_report(row.decisions)
    overall_brier = sum(briers) / len(briers) if briers else calibration.overall_brier_score
    avg_clv = sum(clv_values) / len(clv_values) if clv_values else 0.0
    clv_health = max(0, min(100, 50 + avg_clv * 900))

    roi_values = [s.roi for s in slices if s.roi is not None]
    avg_roi = sum(roi_values) / len(roi_values) if roi_values else 0.0

    readiness = 50.0
    readiness += min(18, len(graded) / 20)
    readiness += max(-15, min(15, avg_roi * 180))
    readiness += max(-12, min(12, (clv_health - 50) * 0.35))
    if calibration.calibration_bias is not None:
        readiness -= min(18, abs(calibration.calibration_bias) * 120)

    warnings = []
    if len(graded) < 100:
        warnings.append("NFL validation sample below promotion threshold.")
    if calibration.calibration_bias is not None and abs(calibration.calibration_bias) >= 0.08:
        warnings.append("NFL calibration bias exceeds target.")
    if clv_health < 45:
        warnings.append("NFL CLV health below target.")

    promotion_ready = len(graded) >= 100 and readiness >= 60 and not any("exceeds" in w or "below target" in w for w in warnings)

    return NflValidationSummary(
        replay_id=row.replay_id,
        model_version=row.model_version,
        total_decisions=len(row.decisions),
        graded_decisions=len(graded),
        market_slices=slices,
        calibration_bias=calibration.calibration_bias,
        overall_brier_score=round(overall_brier, 5) if overall_brier is not None else None,
        clv_health_score=round(clv_health, 2),
        readiness_score=round(max(0, min(100, readiness)), 2),
        promotion_ready=promotion_ready,
        warnings=warnings,
    )
