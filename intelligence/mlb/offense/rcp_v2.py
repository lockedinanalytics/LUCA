from __future__ import annotations

from luca.intelligence.mlb.offense.lineup_chain import score_lineup_chain
from luca.intelligence.mlb.offense.models import RunCreationV2Input, RunCreationV2Output
from luca.intelligence.mlb.offense.platoon import score_platoon_fit


def calculate_rcp_v2(row: RunCreationV2Input) -> RunCreationV2Output:
    warnings: list[str] = []

    chain = score_lineup_chain(row)
    platoon = score_platoon_fit(row.platoon)

    starter_matchup = 100 - row.opposing_starting_pitcher_score * 0.70 + chain.final_chain_score * 0.30
    bullpen_matchup = 100 - row.opposing_bullpen_score * 0.65 + chain.lineup_depth_score * 0.35

    run_env = 50.0
    run_env += (row.park_factor - 1.0) * 35.0
    run_env += row.weather_total_adjustment * 8.0
    run_env += (row.expected_plate_appearances - 38.0) * 1.2

    projected_runs = 4.20
    projected_runs += (chain.final_chain_score - 50) * 0.035
    projected_runs += (platoon.final_platoon_score - 50) * 0.020
    projected_runs += (starter_matchup - 50) * 0.025
    projected_runs += (bullpen_matchup - 50) * 0.018
    projected_runs += (run_env - 50) * 0.018
    projected_runs = max(0.0, projected_runs)

    explosive = 0.18
    explosive += max(0, chain.power_cascade_score - 50) * 0.004
    explosive += max(0, chain.on_base_chain_score - 50) * 0.003
    explosive -= max(0, chain.strikeout_cluster_risk - 55) * 0.002
    explosive = max(0.02, min(0.65, explosive))

    final_rcp = (
        chain.final_chain_score * 0.36
        + platoon.final_platoon_score * 0.16
        + starter_matchup * 0.18
        + bullpen_matchup * 0.14
        + run_env * 0.08
        + (explosive * 100) * 0.08
    )

    warnings.extend(chain.warnings)
    warnings.extend(platoon.warnings)

    populated_hitters = len(row.hitters)
    confidence = 40 + min(45, populated_hitters * 5)
    if populated_hitters < 9:
        confidence -= (9 - populated_hitters) * 3

    explainability = {
        "lineup_chain": round(chain.final_chain_score, 2),
        "platoon": round(platoon.final_platoon_score, 2),
        "starter_matchup": round(starter_matchup, 2),
        "bullpen_matchup": round(bullpen_matchup, 2),
        "run_environment": round(run_env, 2),
        "explosive_inning_probability": round(explosive, 4),
    }

    return RunCreationV2Output(
        lineup_chain_score=chain.final_chain_score,
        platoon_score=platoon.final_platoon_score,
        starter_matchup_score=round(max(0, min(100, starter_matchup)), 2),
        bullpen_matchup_score=round(max(0, min(100, bullpen_matchup)), 2),
        run_environment_score=round(max(0, min(100, run_env)), 2),
        projected_runs=round(projected_runs, 3),
        explosive_inning_probability=round(explosive, 4),
        final_rcp_score=round(max(0, min(100, final_rcp)), 2),
        confidence=round(max(0, min(100, confidence)), 2),
        warnings=warnings,
        explainability=explainability,
    )
