from __future__ import annotations

import math

from luca.intelligence.mlb.environment.models import WeatherVectorInput, WeatherVectorOutput


def _wind_component_out(row: WeatherVectorInput) -> float:
    if row.wind_speed_mph is None or row.wind_direction_degrees is None:
        return 0.0
    # Positive means more aligned with carry toward center field.
    angle_delta = math.radians(row.wind_direction_degrees - row.field_orientation_degrees)
    return row.wind_speed_mph * math.cos(angle_delta)


def score_weather_vector(row: WeatherVectorInput) -> WeatherVectorOutput:
    warnings: list[str] = []

    if row.roof_state.lower() in {"closed", "dome"}:
        return WeatherVectorOutput(
            carry_score=50.0,
            wind_out_score=50.0,
            suppression_score=50.0,
            volatility_score=35.0,
            wind_run_multiplier=1.0,
            total_adjustment=0.0,
            warnings=["Roof closed/dome neutralizes weather impact."],
        )

    carry = 50.0
    suppression = 50.0
    volatility = 40.0

    if row.temperature_f is not None:
        if row.temperature_f >= 85:
            carry += min(10, (row.temperature_f - 80) * 0.45)
        elif row.temperature_f <= 50:
            suppression += min(10, (55 - row.temperature_f) * 0.35)

    if row.humidity_pct is not None:
        carry += (row.humidity_pct - 50) * 0.035

    if row.barometric_pressure_inhg is not None:
        carry += (29.92 - row.barometric_pressure_inhg) * 3.0

    wind_out_component = _wind_component_out(row)
    wind_out_score = 50 + wind_out_component * 1.1
    if abs(wind_out_component) >= 10:
        volatility += 16
        warnings.append("Material wind vector detected.")

    if row.precipitation_probability is not None:
        if row.precipitation_probability >= 45:
            suppression += 6
            volatility += 8
            warnings.append("Precipitation risk can alter offensive environment.")

    wind_run_multiplier = 1.0 + (wind_out_score - 50) / 400.0 + (carry - suppression) / 700.0
    total_adjustment = (carry - 50) * 0.018 + (wind_out_score - 50) * 0.020 - (suppression - 50) * 0.016

    return WeatherVectorOutput(
        carry_score=round(max(0, min(100, carry)), 2),
        wind_out_score=round(max(0, min(100, wind_out_score)), 2),
        suppression_score=round(max(0, min(100, suppression)), 2),
        volatility_score=round(max(0, min(100, volatility)), 2),
        wind_run_multiplier=round(max(0.75, min(1.25, wind_run_multiplier)), 4),
        total_adjustment=round(total_adjustment, 3),
        warnings=warnings,
    )
