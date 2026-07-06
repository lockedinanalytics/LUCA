from __future__ import annotations

from luca.providers.weather.models import WeatherImpact, WeatherSnapshot


def score_weather(snapshot: WeatherSnapshot, roof: str = "open") -> WeatherImpact:
    if not snapshot.available:
        return WeatherImpact(weather_score=50.0, wind_run_multiplier=1.0, total_adjustment=0.0, risk="unknown", notes=snapshot.warnings or ["Weather unavailable."])

    notes: list[str] = []
    score = 50.0
    total_adj = 0.0
    multiplier = 1.0
    risk = "low"

    temp = snapshot.temperature_f
    wind = snapshot.wind_speed_mph or 0.0

    if roof in {"closed", "dome"}:
        return WeatherImpact(weather_score=50.0, wind_run_multiplier=1.0, total_adjustment=0.0, risk="low", notes=["Roof neutralizes most weather."])

    if temp is not None:
        if temp >= 85:
            score += 4
            total_adj += 0.15
            notes.append("Warm air modestly supports carry.")
        elif temp <= 45:
            score -= 4
            total_adj -= 0.15
            notes.append("Cold conditions suppress carry.")

    if wind >= 15:
        risk = "medium"
        multiplier += 0.04
        total_adj += 0.20
        notes.append("Wind speed is material; direction-aware adjustment pending.")
    elif wind >= 10:
        multiplier += 0.02
        total_adj += 0.10
        notes.append("Moderate wind detected.")

    if snapshot.precipitation_probability and snapshot.precipitation_probability > 0:
        risk = "medium"
        score -= 2
        notes.append("Precipitation risk present.")

    return WeatherImpact(weather_score=max(0, min(100, score)), wind_run_multiplier=round(multiplier, 3), total_adjustment=round(total_adj, 3), risk=risk, notes=notes)
