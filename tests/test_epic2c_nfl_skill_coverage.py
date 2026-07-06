from luca.core.models import Sport, TeamGame
from luca.features.mappers.nfl.mapper import NflFeatureMapper
from luca.intelligence.nfl.skill_coverage.coverage import score_coverage_unit
from luca.intelligence.nfl.skill_coverage.matchup import calculate_skill_coverage_matchup
from luca.intelligence.nfl.skill_coverage.models import CoverageUnitInput, ReceiverUnitInput, SkillCoverageMatchupInput


def test_receiver_coverage_matchup_bounds():
    result = calculate_skill_coverage_matchup(SkillCoverageMatchupInput(
        receivers=ReceiverUnitInput(separation_score=61, target_share_score=59, route_participation_score=62),
        coverage=CoverageUnitInput(man_coverage_score=56, zone_coverage_score=58, explosive_pass_prevention_score=55),
    ))
    assert 0 <= result.final_skill_coverage_score <= 100
    assert result.confidence > 0


def test_coverage_bounds():
    result = score_coverage_unit(CoverageUnitInput(man_coverage_score=56, zone_coverage_score=58))
    assert 0 <= result.final_coverage_score <= 100


def test_nfl_mapper_accepts_skill_coverage_v2():
    game = TeamGame(game_id="g1", sport=Sport.NFL, league="NFL", date="2026-09-01", away_team="Away", home_team="Home")
    modules = NflFeatureMapper().build_modules(game, [], context={
        "skill_coverage_v2": {
            "receivers": {"separation_score": 61, "target_share_score": 59, "route_participation_score": 62},
            "coverage": {"man_coverage_score": 56, "zone_coverage_score": 58, "explosive_pass_prevention_score": 55},
        }
    })
    assert "skill_coverage_edge" in modules
    assert "red_zone_skill" in modules
