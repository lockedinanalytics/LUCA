from __future__ import annotations

from luca.intelligence.market.v2.book_disagreement import score_book_disagreement
from luca.intelligence.market.v2.clv import score_clv
from luca.intelligence.market.v2.contradiction import score_market_contradiction
from luca.intelligence.market.v2.line_movement import score_line_movement
from luca.intelligence.market.v2.models import SmartMoneyV2Input, SmartMoneyV2Output
from luca.intelligence.market.v2.steam import score_steam


def calculate_smi_v2(row: SmartMoneyV2Input) -> SmartMoneyV2Output:
    movement = score_line_movement(row.timeline)
    steam = score_steam(row.steam)
    books = score_book_disagreement(row.timeline)
    clv = score_clv(row.clv)
    contradiction = score_market_contradiction(row.contradiction)

    warnings = []
    for block in [movement, steam, books, clv, contradiction]:
        warnings.extend(block.warnings)

    line_movement_score = (
        movement.movement_velocity_score * 0.35
        + movement.directional_strength_score * 0.40
        + movement.late_move_score * 0.25
    )
    steam_score = (
        steam.steam_score * 0.42
        + steam.sharp_alignment_score * 0.33
        + steam.public_divergence_score * 0.25
    )
    book_score = (
        (100 - books.disagreement_score) * 0.20
        + books.best_price_edge_score * 0.25
        + books.consensus_quality_score * 0.25
        + books.liquidity_score * 0.30
    )

    # Contradiction is a penalty, so lower is better.
    final = (
        line_movement_score * 0.24
        + steam_score * 0.24
        + book_score * 0.18
        + clv.clv_score * 0.18
        + (100 - contradiction.contradiction_score) * 0.16
    )

    populated = 0
    total = 0
    for section in [row.timeline, row.steam, row.clv, row.contradiction]:
        data = section.model_dump()
        total += len(data)
        populated += sum(value not in (None, [], {}) for value in data.values())
    confidence = 40 + (populated / total) * 45 if total else 40
    confidence = min(95, confidence * (books.liquidity_score / 75 if books.liquidity_score < 75 else 1.0))

    explainability = {
        "line_movement": round(line_movement_score, 2),
        "steam": round(steam_score, 2),
        "book_disagreement": round(book_score, 2),
        "clv": clv.clv_score,
        "contradiction_penalty": contradiction.contradiction_score,
        "liquidity": books.liquidity_score,
    }

    return SmartMoneyV2Output(
        line_movement_score=round(max(0, min(100, line_movement_score)), 2),
        steam_score=round(max(0, min(100, steam_score)), 2),
        book_disagreement_score=round(max(0, min(100, book_score)), 2),
        clv_score=clv.clv_score,
        contradiction_score=contradiction.contradiction_score,
        liquidity_confidence=books.liquidity_score,
        final_smi_score=round(max(0, min(100, final)), 2),
        confidence=round(max(0, min(100, confidence)), 2),
        warnings=warnings,
        explainability=explainability,
    )
