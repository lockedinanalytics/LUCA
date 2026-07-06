from __future__ import annotations

from fastapi import APIRouter

from luca.intelligence.market.v2.book_disagreement import score_book_disagreement
from luca.intelligence.market.v2.clv import score_clv
from luca.intelligence.market.v2.contradiction import score_market_contradiction
from luca.intelligence.market.v2.engine import calculate_smi_v2
from luca.intelligence.market.v2.line_movement import score_line_movement
from luca.intelligence.market.v2.models import (
    BookLineInput,
    ClvInput,
    MarketContradictionInput,
    MarketTimelineInput,
    SmartMoneyV2Input,
    SteamDetectionInput,
)
from luca.intelligence.market.v2.steam import score_steam

router = APIRouter(prefix="/intelligence/mlb/market", tags=["mlb-market"])


def sample_timeline() -> MarketTimelineInput:
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
            BookLineInput(book="fanduel", odds=-126, is_sharp_book=False, liquidity_score=70),
            BookLineInput(book="pinnacle", odds=-134, is_sharp_book=True, liquidity_score=85),
            BookLineInput(book="circa", odds=-132, is_sharp_book=True, liquidity_score=82),
        ],
    )


@router.get("/line-movement/sample")
async def line_movement_sample():
    return score_line_movement(sample_timeline()).model_dump()


@router.get("/steam/sample")
async def steam_sample():
    return score_steam(SteamDetectionInput(
        line_moves_last_30m=3,
        sharp_books_moved=2,
        total_books_moved=5,
        average_move_size=9,
        public_percent=44,
        sharp_percent=62,
    )).model_dump()


@router.get("/book-disagreement/sample")
async def book_disagreement_sample():
    return score_book_disagreement(sample_timeline()).model_dump()


@router.get("/clv/sample")
async def clv_sample():
    return score_clv(ClvInput(published_odds=-110, closing_odds=-135, projected_probability=0.58)).model_dump()


@router.get("/contradiction/sample")
async def contradiction_sample():
    return score_market_contradiction(MarketContradictionInput(
        model_edge_score=61,
        market_support_score=58,
        public_percent=44,
        sharp_percent=62,
        reverse_line_movement=False,
    )).model_dump()


@router.get("/smi-v2/sample")
async def smi_v2_sample():
    return calculate_smi_v2(SmartMoneyV2Input(
        timeline=sample_timeline(),
        steam=SteamDetectionInput(line_moves_last_30m=3, sharp_books_moved=2, total_books_moved=5, average_move_size=9, public_percent=44, sharp_percent=62),
        clv=ClvInput(published_odds=-110, closing_odds=-135, projected_probability=0.58),
        contradiction=MarketContradictionInput(model_edge_score=61, market_support_score=58, public_percent=44, sharp_percent=62),
    )).model_dump()
