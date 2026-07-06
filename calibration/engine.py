from collections import defaultdict
from luca.ledger.models import LedgerDecision

def confidence_bucket(confidence: float, width: int=5) -> str:
    lo=int(confidence//width)*width
    return f"{lo}-{lo+width-1}"

def build_calibration_summary(decisions: list[LedgerDecision]) -> list[dict]:
    b=defaultdict(lambda: {"plays":0,"wins":0,"losses":0,"units":0.0})
    for d in decisions:
        if d.result not in {"win","loss"}: continue
        r=b[confidence_bucket(d.confidence)]; r["plays"]+=1; r["wins"]+=d.result=="win"; r["losses"]+=d.result=="loss"; r["units"]+=float(d.units_won_lost or 0)
    return [{"bucket":k, **v, "win_pct": v["wins"]/v["plays"] if v["plays"] else None} for k,v in sorted(b.items())]
