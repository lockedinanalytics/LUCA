from __future__ import annotations
from typing import Iterable
from pydantic import BaseModel
from luca.core.models import LucaRunResult

class ReplayResult(BaseModel):
    replay_id: str
    model_version: str
    slates_replayed: int
    recommendations_generated: int
    notes: list[str]

def replay_runs(runs: Iterable[LucaRunResult], model_version: str = "0.4.0") -> ReplayResult:
    rows = list(runs)
    return ReplayResult(
        replay_id=f"replay-{model_version}",
        model_version=model_version,
        slates_replayed=len(rows),
        recommendations_generated=sum(len(row.recommendations) for row in rows),
        notes=["Replay shell created. Historical provider integration required for production replay."],
    )
