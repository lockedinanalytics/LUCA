from __future__ import annotations

from luca.core.math_utils import american_to_implied_probability
from luca.decision.nfl.models import NflUnifiedDecisionInput, NflUnifiedDecisionOutput
from luca.ev.engine import calculate_ev
from luca.simulation.nfl.engine import simulate_nfl_game
from luca.simulation.nfl.models import NflSimulationInput


def _units(score: float, ev: float | None) -> float:
    ev = ev or 0.0
    if score >= 88 and ev >= 0.08:
        return 3.0
    if score >= 82 and ev >= 0.05:
        return 2.0
    if score >= 76 and ev >= 0.03:
        return 1.0
    if score >= 70 and ev > 0:
        return 0.5
    return 0.0


def make_nfl_unified_decision(row: NflUnifiedDecisionInput) -> NflUnifiedDecisionOutput:
    luca_score = (
        row.quarterback_score * 0.24
        + row.trench_score * 0.20
        + row.skill_coverage_score * 0.16
        + row.context_score * 0.14
        + row.market_score * 0.14
        + row.defense_score * 0.07
        + row.injury_score * 0.05
    )

    sim = simulate_nfl_game(NflSimulationInput(
        game_id=row.game_id,
        home_team=row.home_team,
        away_team=row.away_team,
        home_offense_score=(row.quarterback_score * 0.40 + row.trench_score * 0.25 + row.skill_coverage_score * 0.25 + row.context_score * 0.10),
        away_offense_score=50.0,
        home_defense_score=row.defense_score,
        away_defense_score=50.0,
        home_context_score=row.context_score,
        away_context_score=50.0,
        home_market_score=row.market_score,
        away_market_score=50.0,
        home_field_edge=row.home_field_edge,
    ), spread=row.spread, total=row.total)

    if row.market_type == "total":
        probability = sim.over_probability if sim.over_probability is not None else 0.50
    elif row.market_type == "spread":
        probability = sim.spread_cover_probability if sim.spread_cover_probability is not None else sim.home_win_probability
    else:
        probability = sim.home_win_probability if row.selection == row.home_team or row.selection.lower() == "home" else sim.away_win_probability

    # Blend model score probability with simulation probability.
    score_probability = 1 / (1 + 2.718281828 ** (-((luca_score - 50) / 13)))
    projected_probability = probability * 0.62 + score_probability * 0.38

    ev_result = calculate_ev(projected_probability, row.odds, risk_penalty=0.0)
    confidence = max(0, min(100, 50 + (projected_probability - 0.50) * 120 + (luca_score - 50) * 0.35))

    if ev_result.risk_adjusted_ev >= 0.08 and confidence >= 78:
        tier = "strong"
    elif ev_result.risk_adjusted_ev >= 0.04 and confidence >= 70:
        tier = "playable"
    elif ev_result.risk_adjusted_ev > 0:
        tier = "lean"
    else:
        tier = "pass"

    warnings = []
    if sim.margin_variance >= 95:
        warnings.append("High margin variance.")
    if row.market_score < 45:
        warnings.append("Market signal does not support selection.")

    explainability = {
        "quarterback": row.quarterback_score,
        "trench": row.trench_score,
        "skill_coverage": row.skill_coverage_score,
        "context": row.context_score,
        "market": row.market_score,
        "defense": row.defense_score,
        "injury": row.injury_score,
        "implied_probability": round(american_to_implied_probability(row.odds), 5),
    }

    return NflUnifiedDecisionOutput(
        game_id=row.game_id,
        selection=row.selection,
        market_type=row.market_type,
        luca_score=round(luca_score, 2),
        projected_probability=round(projected_probability, 5),
        confidence=round(confidence, 2),
        expected_value=ev_result.risk_adjusted_ev,
        recommendation_tier=tier,
        suggested_units=_units(luca_score, ev_result.risk_adjusted_ev),
        simulation=sim.model_dump(),
        explainability=explainability,
        warnings=warnings,
    )
