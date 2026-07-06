from __future__ import annotations
from luca.core.math_utils import clamp, weighted_average

def universal_power_rating(values: dict[str, float]) -> float:
    return clamp(weighted_average(values, {
        "offense": 0.30, "defense": 0.30, "availability": 0.15,
        "recent_form": 0.10, "coaching": 0.05, "schedule_context": 0.05,
        "market_baseline": 0.05,
    }))

def competitive_advantage(edges: dict[str, float]) -> float:
    return sum(float(edges.get(k, 0.0)) for k in ["talent","health","matchup","rest","coaching","environment","market"])

def volatility_score(values: dict[str, float]) -> float:
    return clamp(weighted_average(values, {
        "simulation_width": 0.25, "injury_uncertainty": 0.20, "weather_risk": 0.15,
        "market_disagreement": 0.15, "style_variance": 0.15, "random_event_risk": 0.10,
    }))

def confidence_integrity(values: dict[str, float]) -> float:
    base = float(values.get("prediction_strength", 75.0))
    penalty = sum(float(values.get(k, 0.0)) for k in [
        "data_uncertainty", "volatility_penalty", "calibration_penalty", "contradiction_penalty"
    ])
    return clamp(base - penalty)

def decision_quality(values: dict[str, float]) -> float:
    return clamp(weighted_average(values, {
        "evidence_quality": 0.25, "model_agreement": 0.20, "positive_ev": 0.20,
        "simulation_stability": 0.15, "calibration_support": 0.10, "explainability": 0.10,
    }))

def luca_composite_intelligence(values: dict[str, float]) -> float:
    return clamp(weighted_average(values, {
        "upr_edge": 0.20, "cae": 0.15, "mde": 0.15, "gce": 0.10,
        "edge": 0.15, "sie": 0.10, "cie": 0.10, "mie": 0.05,
    }))
