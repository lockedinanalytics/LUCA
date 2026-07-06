from __future__ import annotations

from luca.validation.replay.models import ReplayBatch, ReplaySummary


def summarize_replay(batch: ReplayBatch) -> ReplaySummary:
    graded = [d for d in batch.decisions if d.result in {"win", "loss", "push"}]
    wins = sum(d.result == "win" for d in graded)
    losses = sum(d.result == "loss" for d in graded)
    pushes = sum(d.result == "push" for d in graded)
    units = round(sum(float(d.units_won_lost or 0.0) for d in graded), 4)
    risked = sum(float(d.units or 0.0) for d in graded)
    roi = round(units / risked, 5) if risked > 0 else None

    notes = []
    if len(graded) < len(batch.decisions):
        notes.append("Some decisions are ungraded and excluded from ROI.")

    return ReplaySummary(
        replay_id=batch.replay_id,
        model_version=batch.model_version,
        decisions=len(batch.decisions),
        graded_decisions=len(graded),
        wins=wins,
        losses=losses,
        pushes=pushes,
        units=units,
        roi=roi,
        notes=notes,
    )
