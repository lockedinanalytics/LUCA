from __future__ import annotations

from pydantic import BaseModel


class MarketMovementInput(BaseModel):
    opening_odds: float | None = None
    current_odds: float | None = None
    public_percent: float | None = None
    sharp_percent: float | None = None


class MarketMovementOutput(BaseModel):
    smi_score: float
    movement_score: float
    notes: list[str]


def calculate_smi(row: MarketMovementInput) -> MarketMovementOutput:
    score = 50.0
    notes = []
    movement = 0.0

    if row.opening_odds is not None and row.current_odds is not None:
        movement = row.current_odds - row.opening_odds
        if abs(movement) >= 15:
            score += 5 if movement < 0 else -2
            notes.append("Material price movement detected.")

    if row.sharp_percent is not None and row.public_percent is not None:
        diff = row.sharp_percent - row.public_percent
        if diff >= 15:
            score += 8
            notes.append("Sharp/public separation supports selection.")
        elif diff <= -15:
            score -= 6
            notes.append("Sharp/public separation opposes selection.")

    return MarketMovementOutput(smi_score=round(max(0, min(100, score)), 2), movement_score=round(movement, 2), notes=notes)
