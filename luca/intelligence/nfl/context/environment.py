from __future__ import annotations

from luca.intelligence.nfl.context.models import NflEnvironmentInput, NflEnvironmentOutput


def score_nfl_environment(row: NflEnvironmentInput) -> NflEnvironmentOutput:
    warnings: list[str] = []

    if row.roof_state.lower() in {"closed", "dome"}:
        return NflEnvironmentOutput(
            passing_environment_score=56.0,
            rushing_environment_score=50.0,
            kicking_environment_score=56.0,
            weather_risk_score=25.0,
            final_environment_score=54.0,
            warnings=["Closed roof/dome stabilizes environment."],
        )

    passing = 55.0
    rushing = 50.0
    kicking = 55.0
    risk = row.weather_severity_score

    if row.wind_mph is not None:
        passing -= min(18, max(0, row.wind_mph - 8) * 1.1)
        kicking -= min(22, max(0, row.wind_mph - 8) * 1.35)
        if row.wind_mph >= 15:
            warnings.append("Wind materially affects passing and kicking.")

    if row.temperature_f is not None:
        if row.temperature_f <= 25:
            passing -= 5
            kicking -= 6
            rushing += 4
            risk += 8
            warnings.append("Cold-weather adjustment applied.")
        elif row.temperature_f >= 85:
            risk += 4

    if row.precipitation_score < 45:
        passing -= 5
        rushing += 3
        kicking -= 4
        risk += 6
        warnings.append("Precipitation risk affects ball handling.")

    if row.snow_score < 45:
        passing -= 7
        rushing += 5
        kicking -= 7
        risk += 10
        warnings.append("Snow risk detected.")

    passing = passing * 0.82 + row.surface_score * 0.18
    rushing = rushing * 0.70 + row.surface_score * 0.30
    kicking = kicking * 0.78 + row.surface_score * 0.22

    final = passing * 0.32 + rushing * 0.26 + kicking * 0.22 + (100 - risk) * 0.20

    return NflEnvironmentOutput(
        passing_environment_score=round(max(0, min(100, passing)), 2),
        rushing_environment_score=round(max(0, min(100, rushing)), 2),
        kicking_environment_score=round(max(0, min(100, kicking)), 2),
        weather_risk_score=round(max(0, min(100, risk)), 2),
        final_environment_score=round(max(0, min(100, final)), 2),
        warnings=warnings,
    )
