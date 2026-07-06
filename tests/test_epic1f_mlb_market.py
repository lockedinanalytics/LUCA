from luca.core.models import Sport, TeamGame
from luca.features.mappers.mlb import MlbFeatureMapper
from luca.intelligence.market.v2.book_disagreement import score_book_disagreement
from luca.intelligence.market.v2.clv import score_clv
from luca.intelligence.market.v2.contradiction import score_market_contradiction
from luca.intelligence.market.v2.engine import calculate_smi_v2
from luca.intelligence.market.v2.line_movement import score_line_movement
from luca.intelligence.market.v2.models import BookLineInput, ClvInput, MarketContradictionInput, MarketTimelineInput, SmartMoneyV2Input, SteamDetectionInput
from luca.intelligence.market.v2.steam import score_steam


def timeline():
    return MarketTimelineInput(
        market="moneyline",
        selection="Home",
        opening_odds=-110,
        current_odds=-128,
        closing_odds=-135,
        minutes_since_open=720,
        minutes_to_start=90,
        books=[
            BookLineInput(book="draftkings", odds=-128, is_sharp_book=False, liquidity_score=70),
            BookLineInput(book="pinnacle", odds=-134, is_sharp_book=True, liquidity_score=85),
        ],
    )


def test_line_movement_bounds():
    result = score_line_movement(timeline())
    assert 0 <= result.movement_velocity_score <= 100


def test_steam_bounds():
    result = score_steam(SteamDetectionInput(line_moves_last_30m=3, sharp_books_moved=2, total_books_moved=5, average_move_size=9))
    assert 0 <= result.steam_score <= 100


def test_book_disagreement_bounds():
    result = score_book_disagreement(timeline())
    assert 0 <= result.consensus_quality_score <= 100


def test_clv_bounds():
    result = score_clv(ClvInput(published_odds=-110, closing_odds=-135, projected_probability=0.58))
    assert 0 <= result.clv_score <= 100


def test_contradiction_bounds():
    result = score_market_contradiction(MarketContradictionInput(model_edge_score=61, market_support_score=58))
    assert 0 <= result.contradiction_score <= 100


def test_smi_v2_bounds():
    result = calculate_smi_v2(SmartMoneyV2Input(
        timeline=timeline(),
        steam=SteamDetectionInput(line_moves_last_30m=3, sharp_books_moved=2, total_books_moved=5, average_move_size=9, public_percent=44, sharp_percent=62),
        clv=ClvInput(published_odds=-110, closing_odds=-135, projected_probability=0.58),
        contradiction=MarketContradictionInput(model_edge_score=61, market_support_score=58, public_percent=44, sharp_percent=62),
    ))
    assert 0 <= result.final_smi_score <= 100
    assert result.confidence > 0


def test_mapper_accepts_market_v2():
    game = TeamGame(game_id="g1", sport=Sport.MLB, league="MLB", date="2026-07-04", away_team="Away", home_team="Home")
    modules = MlbFeatureMapper().build_modules(game, [], context={
        "market_v2": {
            "timeline": timeline().model_dump(),
            "steam": {"line_moves_last_30m": 3, "sharp_books_moved": 2, "total_books_moved": 5, "average_move_size": 9, "public_percent": 44, "sharp_percent": 62},
            "clv": {"published_odds": -110, "closing_odds": -135, "projected_probability": 0.58},
            "contradiction": {"model_edge_score": 61, "market_support_score": 58}
        }
    })
    assert "smi" in modules
    assert modules["smi"] > 0
