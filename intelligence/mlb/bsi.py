from __future__ import annotations

from pydantic import BaseModel


class BullpenUsageInput(BaseModel):
    total_pitches_yesterday: int = 0
    total_pitches_last_3_days: int = 0
    back_to_back_relievers: int = 0
    closer_available: bool = True
    setup_available: bool = True


class BullpenStressOutput(BaseModel):
    availability_score: float
    fatigue_score: float
    leverage_availability: float
    final_bsi: float
    notes: list[str]


def calculate_bsi(row: BullpenUsageInput) -> BullpenStressOutput:
    notes = []
    availability = 70.0
    fatigue = 70.0

    fatigue -= min(25, row.total_pitches_yesterday * 0.08)
    fatigue -= min(25, row.total_pitches_last_3_days * 0.035)
    fatigue -= row.back_to_back_relievers * 4

    if not row.closer_available:
        availability -= 12
        notes.append("Closer unavailable.")
    if not row.setup_available:
        availability -= 8
        notes.append("Setup arm unavailable.")

    leverage = availability * 0.60 + fatigue * 0.40
    final = max(0, min(100, availability * 0.35 + fatigue * 0.35 + leverage * 0.30))

    return BullpenStressOutput(
        availability_score=round(max(0, min(100, availability)), 2),
        fatigue_score=round(max(0, min(100, fatigue)), 2),
        leverage_availability=round(max(0, min(100, leverage)), 2),
        final_bsi=round(final, 2),
        notes=notes,
    )
