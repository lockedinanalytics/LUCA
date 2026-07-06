from luca.core.models import Sport, TeamGame
from luca.features.mappers.mlb import MlbFeatureMapper
from luca.intelligence.mlb.offense.hitter import score_hitter
from luca.intelligence.mlb.offense.lineup_chain import score_lineup_chain
from luca.intelligence.mlb.offense.models import HitterInput, LineupChainInput, PlatoonInput, RunCreationV2Input
from luca.intelligence.mlb.offense.platoon import score_platoon_fit
from luca.intelligence.mlb.offense.rcp_v2 import calculate_rcp_v2


def hitters():
    return [
        HitterInput(name=f"H{i}", lineup_spot=i, xwoba_score=55+i, xslg_score=54+i, hard_hit_score=53+i, contact_score=52+i, platoon_score=51+i, pitch_type_fit_score=52+i)
        for i in range(1, 10)
    ]


def test_hitter_score_bounds():
    result = score_hitter(hitters()[2])
    assert 0 <= result.final_hitter_score <= 100


def test_lineup_chain_bounds():
    result = score_lineup_chain(LineupChainInput(hitters=hitters(), bench_score=54, pinch_hit_score=55))
    assert 0 <= result.final_chain_score <= 100
    assert len(result.hitter_scores) == 9


def test_platoon_bounds():
    result = score_platoon_fit(PlatoonInput(projected_lhp_plate_appearances=12, projected_rhp_plate_appearances=26, lineup_platoon_score=56))
    assert 0 <= result.final_platoon_score <= 100


def test_rcp_v2_output():
    result = calculate_rcp_v2(RunCreationV2Input(hitters=hitters(), bench_score=54, platoon=PlatoonInput(lineup_platoon_score=56), opposing_starting_pitcher_score=55, opposing_bullpen_score=52))
    assert result.projected_runs > 0
    assert 0 <= result.final_rcp_score <= 100


def test_mapper_accepts_offense_v2():
    game = TeamGame(game_id="g1", sport=Sport.MLB, league="MLB", date="2026-07-04", away_team="Away", home_team="Home")
    modules = MlbFeatureMapper().build_modules(game, [], context={"offense_v2": {"hitters": [h.model_dump() for h in hitters()]}})
    assert "rcp" in modules
    assert modules["rcp"] > 0
