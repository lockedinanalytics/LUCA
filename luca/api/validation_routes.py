from __future__ import annotations

from fastapi import APIRouter

from luca.validation.drift.engine import build_drift_report
from luca.validation.replay.models import HistoricalDecision, ReplayBatch
from luca.validation.reports.engine import build_validation_report

router = APIRouter(prefix="/validation", tags=["validation"])


def sample_decisions() -> list[HistoricalDecision]:
    rows = []
    for i in range(1, 41):
        win = i % 3 != 0
        confidence = 58 + (i % 8) * 4
        rows.append(HistoricalDecision(
            decision_id=f"d{i}",
            date="2026-07-04",
            sport="mlb",
            league="MLB",
            game_id=f"g{i}",
            market="moneyline" if i % 2 else "total",
            category="presidential" if i % 10 == 0 else "cabinet",
            selection="Home",
            odds=-110,
            units=1.0,
            confidence=confidence,
            projected_probability=confidence / 100,
            luca_score=confidence + 3,
            result="win" if win else "loss",
            units_won_lost=0.91 if win else -1.0,
            closing_odds=-120 if win else -105,
            module_snapshot={
                "sp": 55 + (i % 7),
                "bsi": 54 + (i % 5),
                "rcp": 53 + (i % 6),
                "smi": 52 + (i % 8),
                "cam": 50 + (i % 4),
            },
        ))
    return rows


@router.get("/report/sample")
async def validation_report_sample():
    return build_validation_report(ReplayBatch(replay_id="sample", model_version="1.0.0-epic1g", decisions=sample_decisions())).model_dump()


@router.get("/drift/sample")
async def drift_sample():
    baseline = sample_decisions()[:20]
    current = sample_decisions()[20:]
    for row in current:
        row.module_snapshot["smi"] += 8
    return build_drift_report(baseline, current).model_dump()
