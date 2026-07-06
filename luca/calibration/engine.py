from __future__ import annotations
from collections import defaultdict
from typing import Iterable
from luca.ledger.models import LedgerDecision

def confidence_bucket(confidence: float, width: int = 5) -> str:
    lower = int(confidence // width) * width
    return f"{lower}-{lower + width - 1}"

def build_calibration_summary(decisions: Iterable[LedgerDecision]) -> list[dict]:
    buckets = defaultdict(lambda: {"plays": 0, "wins": 0, "losses": 0, "units": 0.0, "clv": []})
    for d in decisions:
        if d.result not in {"win", "loss"}:
            continue
        row = buckets[confidence_bucket(d.confidence)]
        row["plays"] += 1
        row["wins"] += 1 if d.result == "win" else 0
        row["losses"] += 1 if d.result == "loss" else 0
        row["units"] += float(d.units_won_lost or 0.0)
        if d.clv is not None:
            row["clv"].append(float(d.clv))
    return [{"bucket": b, "plays": r["plays"], "wins": r["wins"], "losses": r["losses"],
             "win_pct": r["wins"] / r["plays"] if r["plays"] else None, "units": r["units"],
             "avg_clv": sum(r["clv"]) / len(r["clv"]) if r["clv"] else None}
            for b, r in sorted(buckets.items())]
