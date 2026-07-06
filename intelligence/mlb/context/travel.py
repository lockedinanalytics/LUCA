from __future__ import annotations

from luca.intelligence.mlb.environment.models import TravelContextInput, TravelContextOutput


def score_travel_context(row: TravelContextInput) -> TravelContextOutput:
    warnings: list[str] = []

    fatigue = 65.0
    fatigue -= min(18, row.miles_traveled_last_3_days / 180.0)
    fatigue -= min(10, abs(row.time_zone_shift) * 3.0)
    fatigue -= min(12, row.consecutive_road_games * 1.25)
    fatigue += min(8, row.rest_days * 4.0)

    circadian = 60.0 - min(14, abs(row.time_zone_shift) * 4.0)
    pressure = 60.0
    if row.getaway_game:
        pressure -= 6
        warnings.append("Getaway-game context can affect lineup and bullpen usage.")
    if row.doubleheader:
        pressure -= 10
        warnings.append("Doubleheader creates roster and bullpen strain.")
    pressure = pressure * 0.75 + row.bullpen_travel_load_score * 0.25

    if row.miles_traveled_last_3_days >= 1800:
        warnings.append("High travel mileage detected.")
    if row.consecutive_road_games >= 6:
        warnings.append("Extended road trip detected.")

    final = fatigue * 0.45 + circadian * 0.25 + pressure * 0.30

    return TravelContextOutput(
        fatigue_score=round(max(0, min(100, fatigue)), 2),
        circadian_score=round(max(0, min(100, circadian)), 2),
        schedule_pressure_score=round(max(0, min(100, pressure)), 2),
        travel_context_score=round(max(0, min(100, final)), 2),
        warnings=warnings,
    )
