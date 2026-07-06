from __future__ import annotations

from luca.intelligence.nfl.trench.defensive_front import score_defensive_front
from luca.intelligence.nfl.trench.models import TrenchMatchupInput, TrenchMatchupOutput
from luca.intelligence.nfl.trench.offensive_line import score_offensive_line


def calculate_trench_matchup(row: TrenchMatchupInput) -> TrenchMatchupOutput:
    ol = score_offensive_line(row.offensive_line)
    front = score_defensive_front(row.defensive_front)

    warnings = []
    warnings.extend(ol.warnings)
    warnings.extend(front.warnings)

    pass_edge = (
        ol.pass_protection_score * 0.46
        + row.quarterback_pressure_resilience_score * 0.18
        + row.offensive_scheme_score * 0.14
        + (100 - front.pass_rush_score) * 0.22
    )

    run_edge = (
        ol.run_blocking_score * 0.36
        + row.running_back_vision_score * 0.16
        + row.offensive_scheme_score * 0.13
        + (100 - front.run_defense_score) * 0.24
        + row.weather_surface_score * 0.11
    )

    pressure_projection = (
        front.pass_rush_score * 0.42
        + front.disruption_score * 0.24
        + (100 - ol.pass_protection_score) * 0.24
        + (100 - row.quarterback_pressure_resilience_score) * 0.10
    )

    sack_projection = (
        pressure_projection * 0.46
        + (100 - row.quarterback_pressure_resilience_score) * 0.20
        + (100 - ol.continuity_health_score) * 0.18
        + front.disruption_score * 0.16
    )

    rushing_efficiency = run_edge * 0.52 + ol.short_yardage_score * 0.18 + (100 - front.containment_score) * 0.18 + row.weather_surface_score * 0.12
    explosive_run = (
        run_edge * 0.38
        + (100 - front.containment_score) * 0.26
        + row.running_back_vision_score * 0.20
        + row.offensive_scheme_score * 0.16
    )

    short_yardage = (
        ol.short_yardage_score * 0.42
        + (100 - front.run_defense_score) * 0.26
        + row.offensive_scheme_score * 0.16
        + (100 - row.defensive_scheme_score) * 0.16
    )

    red_zone = (
        short_yardage * 0.34
        + pass_edge * 0.20
        + run_edge * 0.22
        + ol.continuity_health_score * 0.12
        + row.offensive_scheme_score * 0.12
    )

    # Final score is offense-facing trench edge.
    final = (
        pass_edge * 0.26
        + run_edge * 0.24
        + rushing_efficiency * 0.16
        + short_yardage * 0.12
        + red_zone * 0.12
        + (100 - pressure_projection) * 0.10
    )

    populated = 0
    total = 0
    for section in [row.offensive_line, row.defensive_front, row]:
        data = section.model_dump()
        total += len(data)
        populated += sum(v is not None for v in data.values())
    confidence = 45 + min(45, populated / max(1, total) * 45)
    if warnings:
        confidence -= min(10, len(warnings))

    explainability = {
        "offensive_line": ol.final_ol_score,
        "defensive_front": front.final_front_score,
        "pass_edge": round(pass_edge, 2),
        "run_edge": round(run_edge, 2),
        "pressure_projection": round(pressure_projection, 2),
        "sack_projection": round(sack_projection, 2),
        "rushing_efficiency": round(rushing_efficiency, 2),
    }

    return TrenchMatchupOutput(
        offensive_line_score=ol.final_ol_score,
        defensive_front_score=front.final_front_score,
        pass_protection_edge=round(max(0, min(100, pass_edge)), 2),
        run_blocking_edge=round(max(0, min(100, run_edge)), 2),
        pressure_projection_score=round(max(0, min(100, pressure_projection)), 2),
        sack_projection_score=round(max(0, min(100, sack_projection)), 2),
        rushing_efficiency_projection=round(max(0, min(100, rushing_efficiency)), 2),
        explosive_run_probability_score=round(max(0, min(100, explosive_run)), 2),
        short_yardage_advantage_score=round(max(0, min(100, short_yardage)), 2),
        red_zone_trench_score=round(max(0, min(100, red_zone)), 2),
        final_trench_score=round(max(0, min(100, final)), 2),
        confidence=round(max(0, min(100, confidence)), 2),
        warnings=warnings,
        explainability=explainability,
    )
