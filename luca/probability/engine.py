from __future__ import annotations

from math import exp, log
from pydantic import BaseModel


class ProbabilityResult(BaseModel):
    raw_probability: float
    calibrated_probability: float
    confidence_interval_low: float
    confidence_interval_high: float
    notes: list[str]


def logistic_probability(score: float, midpoint: float = 50.0, scale: float = 12.0) -> float:
    return 1.0 / (1.0 + exp(-((float(score) - midpoint) / scale)))


def bayesian_update(prior: float, evidence_probability: float, evidence_weight: float = 0.35) -> float:
    prior = min(max(prior, 0.001), 0.999)
    evidence_probability = min(max(evidence_probability, 0.001), 0.999)
    evidence_weight = min(max(evidence_weight, 0.0), 1.0)
    prior_logit = log(prior / (1 - prior))
    evidence_logit = log(evidence_probability / (1 - evidence_probability))
    updated_logit = (1 - evidence_weight) * prior_logit + evidence_weight * evidence_logit
    return 1.0 / (1.0 + exp(-updated_logit))


def confidence_interval(probability: float, volatility: float = 0.12) -> tuple[float, float]:
    volatility = min(max(volatility, 0.01), 0.35)
    low = max(0.0, probability - volatility)
    high = min(1.0, probability + volatility)
    return low, high


def probability_from_luca_score(score: float, evidence_probability: float | None = None, volatility: float = 0.12) -> ProbabilityResult:
    raw = logistic_probability(score)
    calibrated = bayesian_update(raw, evidence_probability, 0.30) if evidence_probability is not None else raw
    low, high = confidence_interval(calibrated, volatility)
    return ProbabilityResult(
        raw_probability=round(raw, 5),
        calibrated_probability=round(calibrated, 5),
        confidence_interval_low=round(low, 5),
        confidence_interval_high=round(high, 5),
        notes=["Phase 5 probability engine: logistic baseline with optional Bayesian evidence update."],
    )
