from luca.core.models import Sport, TeamGame
from luca.features.mappers.nfl.mapper import NflFeatureMapper
from luca.intelligence.nfl.quarterback.engine import calculate_nfl_quarterback_intelligence
from luca.intelligence.nfl.quarterback.models import (
    NflQuarterbackDecisionInput,
    NflQuarterbackEfficiencyInput,
    NflQuarterbackExplosiveInput,
    NflQuarterbackIntelligenceInput,
    NflQuarterbackPressureInput,
)


def test_qb_engine_bounds():
    result = calculate_nfl_quarterback_intelligence(NflQuarterbackIntelligenceInput(
        efficiency=NflQuarterbackEfficiencyInput(epa_per_play=0.16, success_rate=48.5, cpoe=2.8, anya=7.4),
        explosive=NflQuarterbackExplosiveInput(explosive_pass_rate=14.5, air_yards_per_attempt=8.3, big_time_throw_rate=5.6),
        pressure=NflQuarterbackPressureInput(pressure_epa_per_play=-0.08, pressure_to_sack_rate=17.5),
        decision=NflQuarterbackDecisionInput(turnover_worthy_play_rate=2.8, interception_rate=1.8),
    ))
    assert 0 <= result.final_qb_score <= 100
    assert result.confidence > 0


def test_nfl_mapper_accepts_quarterback_v2():
    game = TeamGame(game_id="g1", sport=Sport.NFL, league="NFL", date="2026-09-01", away_team="Away", home_team="Home")
    mapper = NflFeatureMapper()
    modules = mapper.build_modules(game, [], context={
        "quarterback_v2": {
            "efficiency": {"epa_per_play": 0.16, "success_rate": 48.5, "cpoe": 2.8, "anya": 7.4},
            "explosive": {"explosive_pass_rate": 14.5, "air_yards_per_attempt": 8.3, "big_time_throw_rate": 5.6},
            "pressure": {"pressure_epa_per_play": -0.08, "pressure_to_sack_rate": 17.5},
            "decision": {"turnover_worthy_play_rate": 2.8, "interception_rate": 1.8},
        }
    })
    assert "qb_edge" in modules
    assert modules["qb_edge"] > 0
