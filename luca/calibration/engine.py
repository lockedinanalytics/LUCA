from __future__ import annotations

from collections import defaultdict
from typing import Iterable

from luca.ledger.models import LedgerDecision


def confidence_bucket(confidence: float, width: int = 5) -> str:
    lower = int(confidence // width) * width
    upper = lower + width - 1
    return f"{lower}-{upper}"


def build_calibration_summary(decisions: Iterable[LedgerDecision]) -> list[dict]:
    buckets = defaultdict(lambda: {"plays": 0, "wins": 0, "losses": 0, "units": 0.0, "clv": []})
    for d in decisions:
        if d.result not in {"win", "loss"}:
            continue
        bucket = confidence_bucket(d.confidence)
        row = buckets[bucket]
        row["plays"] += 1
        row["wins"] += 1 if d.result == "win" else 0
        row["losses"] += 1 if d.result == "loss" else 0
        row["units"] += float(d.units_won_lost or 0.0)
        if d.clv is not None:
            row["clv"].append(float(d.clv))

    output = []
    for bucket, row in sorted(buckets.items()):
        plays = row["plays"]
        avg_clv = sum(row["clv"]) / len(row["clv"]) if row["clv"] else None
        output.append({
            "bucket": bucket,
            "plays": plays,
            "wins": row["wins"],
            "losses": row["losses"],
            "win_pct": row["wins"] / plays if plays else None,
            "units": row["units"],
            "avg_clv": avg_clv,
        })
    return output
