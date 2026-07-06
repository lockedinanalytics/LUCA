from luca.probability.engine import probability_from_luca_score
from luca.simulation.distributions.score_distribution import ScoreDistributionRequest, simulate_score_distribution
from luca.evidence.fusion import EvidenceInput, fuse_evidence
from luca.intelligence.mlb.starting_pitcher import StartingPitcherInput, calculate_starting_pitcher_score
from luca.intelligence.mlb.lineup_quality import LineupQualityInput, calculate_lineup_quality
from luca.trace.decision_trace import build_decision_trace
from luca.core.models import GovernanceStatus, MarketType, PickCategory, PickRecommendation, Sport


def test_probability_engine():
    result = probability_from_luca_score(58, evidence_probability=0.56)
    assert 0 <= result.calibrated_probability <= 1


def test_score_distribution():
    result = simulate_score_distribution(ScoreDistributionRequest(game_id="x", home_mean=4.5, away_mean=4.0, runs=500))
    assert 0 <= result.home_win_probability <= 1


def test_evidence_fusion():
    result = fuse_evidence(EvidenceInput(module_scores={"a": 60, "b": 55}, module_weights={"a": .6, "b": .4}))
    assert result.fused_score > 0


def test_starting_pitcher():
    result = calculate_starting_pitcher_score(StartingPitcherInput(xera=3.7, fip=3.8, strikeout_rate=26, walk_rate=7))
    assert 0 <= result.final_sp_score <= 100


def test_lineup_quality():
    result = calculate_lineup_quality(LineupQualityInput(top_four_xwoba_score=60, bottom_five_xwoba_score=52))
    assert 0 <= result.final_lineup_score <= 100


def test_decision_trace():
    pick = PickRecommendation(
        category=PickCategory.CABINET,
        sport=Sport.MLB,
        league="MLB",
        game_id="g1",
        market_type=MarketType.MONEYLINE,
        selection="Home",
        confidence=80,
        units=1,
        governance_status=GovernanceStatus.APPROVED,
        audit={"modules": {"sp": 60, "bsi": 52, "rcp": 58}},
    )
    trace = build_decision_trace("d1", pick)
    assert trace.decision_id == "d1"
