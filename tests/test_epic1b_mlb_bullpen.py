from luca.core.models import Sport, TeamGame
from luca.features.mappers.mlb import MlbFeatureMapper
from luca.intelligence.mlb.bullpen.availability import score_reliever_availability
from luca.intelligence.mlb.bullpen.collapse import score_bullpen_collapse
from luca.intelligence.mlb.bullpen.engine import calculate_bullpen_intelligence
from luca.intelligence.mlb.bullpen.hierarchy import score_bullpen_hierarchy
from luca.intelligence.mlb.bullpen.models import BullpenCollapseInput, BullpenHierarchyInput, BullpenIntelligenceInput, RelieverUsageInput


def sample_relievers():
    return [
        RelieverUsageInput(name="Closer A", role="closer", pitches_yesterday=18, pitches_last_3_days=42, appearances_last_3_days=2, leverage_role_score=82, season_quality_score=76, recent_quality_score=74, inherited_runner_score=70, command_volatility_score=68),
        RelieverUsageInput(name="Setup B", role="setup", pitches_yesterday=0, pitches_last_3_days=24, appearances_last_3_days=1, leverage_role_score=76, season_quality_score=70, recent_quality_score=72, inherited_runner_score=66, command_volatility_score=64),
        RelieverUsageInput(name="Lefty C", role="primary_lefty", pitches_yesterday=12, pitches_last_3_days=28, appearances_last_3_days=2, leverage_role_score=68, season_quality_score=64, recent_quality_score=60, inherited_runner_score=62, command_volatility_score=58),
    ]


def test_reliever_availability_bounds():
    result = score_reliever_availability(sample_relievers()[0])
    assert 0 <= result.availability_score <= 100
    assert result.name == "Closer A"


def test_hierarchy_output():
    result = score_bullpen_hierarchy(BullpenHierarchyInput(relievers=sample_relievers()))
    assert result.available_total_count >= 1


def test_collapse_output():
    result = score_bullpen_collapse(BullpenCollapseInput(
        available_total_count=3,
        available_high_leverage_count=2,
        bullpen_quality_score=66,
        fatigue_score=62,
        command_volatility_score=60,
        inherited_runner_score=64,
    ))
    assert 0 <= result.collapse_probability_score <= 100


def test_bullpen_intelligence():
    result = calculate_bullpen_intelligence(BullpenIntelligenceInput(relievers=sample_relievers(), manager_usage_score=55))
    assert 0 <= result.final_bsi <= 100
    assert result.confidence > 40


def test_mlb_mapper_accepts_bullpen_v2_context():
    game = TeamGame(game_id="g1", sport=Sport.MLB, league="MLB", date="2026-07-04", away_team="Away", home_team="Home")
    mapper = MlbFeatureMapper()
    modules = mapper.build_modules(game, [], context={"bullpen_v2": {"relievers": [r.model_dump() for r in sample_relievers()], "manager_usage_score": 55}})
    assert "bsi" in modules
    assert modules["bsi"] > 0
