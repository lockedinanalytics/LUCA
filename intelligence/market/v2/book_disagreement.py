from __future__ import annotations

from statistics import mean, pstdev

from luca.intelligence.market.v2.models import BookDisagreementOutput, MarketTimelineInput
from luca.intelligence.market.v2.utils import clamp


def score_book_disagreement(row: MarketTimelineInput) -> BookDisagreementOutput:
    warnings: list[str] = []
    priced = [book for book in row.books if book.odds is not None]

    if not priced:
        return BookDisagreementOutput(
            disagreement_score=50.0,
            best_price_edge_score=50.0,
            consensus_quality_score=35.0,
            liquidity_score=35.0,
            warnings=["No book-level prices supplied."],
        )

    odds_values = [float(book.odds) for book in priced]
    dispersion = pstdev(odds_values) if len(odds_values) > 1 else 0.0
    disagreement = 50 + min(35, dispersion * 0.45)

    current = row.current_odds if row.current_odds is not None else mean(odds_values)
    best = max(odds_values)
    worst = min(odds_values)
    best_price_edge = 50 + min(30, abs(best - current) * 0.35)

    sharp_books = [book for book in priced if book.is_sharp_book]
    if sharp_books:
        sharp_avg = mean([float(book.odds) for book in sharp_books])
        broad_avg = mean(odds_values)
        if abs(sharp_avg - broad_avg) >= 12:
            warnings.append("Sharp-book average differs from broad market.")

    liquidity = mean([book.liquidity_score for book in priced])
    consensus = 100 - min(45, dispersion * 0.40)
    if dispersion >= 25:
        warnings.append("High book disagreement increases price sensitivity.")

    return BookDisagreementOutput(
        disagreement_score=round(clamp(disagreement), 2),
        best_price_edge_score=round(clamp(best_price_edge), 2),
        consensus_quality_score=round(clamp(consensus), 2),
        liquidity_score=round(clamp(liquidity), 2),
        warnings=warnings,
    )
