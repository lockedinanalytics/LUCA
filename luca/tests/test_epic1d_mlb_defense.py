from luca.core.models import Sport, TeamGame
from luca.features.mappers.mlb import MlbFeatureMapper
from luca.intelligence.mlb.defense.baserunning import score_baserunner_prevention
from luca.intelligence.mlb.defense.catcher import score_catcher
from luca.intelligence.mlb.defense.engine import calculate_defensive_intelligence
from luca.intelligence.mlb.defense.fielding import score_fielding_unit
from luca.intelligence.mlb.defense.models import BaserunnerPreventionInput, CatcherInput, DefensiveIntelligenceInput, FieldingUnitInput


def test_catcher_score_bounds():
    result = score_catcher(CatcherInput(name="C", framing_score=62, blocking_score=58, throwing_score=56))
    assert 0 <= result.final_cam_score <= 100


def test_fielding_score_bounds():
    result = score_fielding_unit(FieldingUnitInput(infield_oaa_score=58, outfield_oaa_score=56, drs_score=57))
    assert 0 <= result.final_fielding_score <= 100


def test_baserunner_prevention_bounds():
    result = score_baserunner_prevention(BaserunnerPreventionInput(catcher_throwing_score=56, pitcher_hold_score=54, outfield_arm_score=57))
    assert 0 <= result.pressure_adjusted_score <= 100


def test_defensive_intelligence_bounds():
    result = calculate_defensive_intelligence(DefensiveIntelligenceInput(
        catcher=CatcherInput(name="C", framing_score=62, blocking_score=58, throwing_score=56),
        fielding=FieldingUnitInput(infield_oaa_score=58, outfield_oaa_score=56, drs_score=57),
        baserunner_prevention=BaserunnerPreventionInput(catcher_throwing_score=56, pitcher_hold_score=54),
    ))
    assert 0 <= result.defensive_run_prevention_score <= 100
    assert result.cam_score > 0


def test_mapper_accepts_defense_v2():
    game = TeamGame(game_id="g1", sport=Sport.MLB, league="MLB", date="2026-07-04", away_team="Away", home_team="Home")
    modules = MlbFeatureMapper().build_modules(game, [], context={
        "defense_v2": {
            "catcher": {"name": "C", "framing_score": 62, "blocking_score": 58, "throwing_score": 56},
            "fielding": {"infield_oaa_score": 58, "outfield_oaa_score": 56, "drs_score": 57},
            "baserunner_prevention": {"catcher_throwing_score": 56, "pitcher_hold_score": 54}
        }
    })
    assert "cam" in modules
    assert "defense_support" in modules
