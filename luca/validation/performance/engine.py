from __future__ import annotations

from collections import defaultdict

from luca.validation.performance.models import PerformanceReport, PerformanceSlice
from luca.validation.replay.models import HistoricalDecision


def _slice(decisions: list[HistoricalDecision], attr: str) -> list[PerformanceSlice]:
    grouped = defaultdict(list)
    for d in decisions:
        grouped[str(getattr(d, attr))].append(d)

    out = []
    for key, rows in sorted(grouped.items()):
        graded = [d for d in rows if d.result in {"win", "loss", "push"}]
        wins = sum(d.result == "win" for d in graded)
        losses = sum(d.result == "loss" for d in graded)
        pushes = sum(d.result == "push" for d in graded)
        units = round(sum(float(d.units_won_lost or 0.0) for d in graded), 4)
        risked = sum(float(d.units or 0.0) for d in graded)
        roi = round(units / risked, 5) if risked > 0 else None
        win_rate = round(wins / (wins + losses), 5) if wins + losses > 0 else None
        out.append(PerformanceSlice(key=key, decisions=len(graded), wins=wins, losses=losses, pushes=pushes, units=units, risked=round(risked, 3), roi=roi, win_rate=win_rate))
    return out


def build_performance_report(decisions: list[HistoricalDecision]) -> PerformanceReport:
    return PerformanceReport(
        by_category=_slice(decisions, "category"),
        by_market=_slice(decisions, "market"),
        by_sport=_slice(decisions, "sport"),
        by_league=_slice(decisions, "league"),
    )
