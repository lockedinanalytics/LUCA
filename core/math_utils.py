from __future__ import annotations
from math import exp

def clamp(value: float, low: float=0.0, high: float=100.0) -> float:
    return max(low, min(high, float(value)))

def weighted_average(values: dict[str, float], weights: dict[str, float], default: float=50.0) -> float:
    total = sum(weights.values())
    if total <= 0:
        return default
    return sum(float(values.get(k, default))*w for k,w in weights.items()) / total

def american_to_implied_probability(odds: float) -> float:
    odds = float(odds)
    return abs(odds)/(abs(odds)+100.0) if odds < 0 else 100.0/(odds+100.0)

def probability_to_american(probability: float) -> float:
    p = min(max(float(probability), .0001), .9999)
    return -100*p/(1-p) if p >= .5 else 100*(1-p)/p

def logistic(x: float) -> float:
    return 1/(1+exp(-float(x)))
