from __future__ import annotations
from luca.core.math_utils import clamp, weighted_average

def universal_power_rating(values: dict[str,float]) -> float:
    return clamp(weighted_average(values, {"offense":.30,"defense":.30,"availability":.15,"recent_form":.10,"coaching":.05,"schedule_context":.05,"market_baseline":.05}))

def confidence_integrity(values: dict[str,float]) -> float:
    base = float(values.get("prediction_strength", 75))
    penalty = sum(float(values.get(k,0)) for k in ["data_uncertainty","volatility_penalty","calibration_penalty","contradiction_penalty"])
    return clamp(base - penalty)

def decision_quality(values: dict[str,float]) -> float:
    return clamp(weighted_average(values, {"evidence_quality":.25,"model_agreement":.20,"positive_ev":.20,"simulation_stability":.15,"calibration_support":.10,"explainability":.10}))

def luca_composite_intelligence(values: dict[str,float]) -> float:
    return clamp(weighted_average(values, {"upr_edge":.20,"cae":.15,"mde":.15,"gce":.10,"edge":.15,"sie":.10,"cie":.10,"mie":.05}))
