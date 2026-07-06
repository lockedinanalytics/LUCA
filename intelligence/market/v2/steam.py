from __future__ import annotations

from luca.intelligence.market.v2.models import SteamDetectionInput, SteamDetectionOutput
from luca.intelligence.market.v2.utils import clamp


def score_steam(row: SteamDetectionInput) -> SteamDetectionOutput:
    warnings: list[str] = []

    steam = 50.0
    steam += min(20, row.line_moves_last_30m * 3.0)
    steam += min(18, row.sharp_books_moved * 4.0)
    steam += min(12, row.average_move_size * 1.2)

    sharp_alignment = 50.0
    if row.total_books_moved > 0:
        sharp_ratio = row.sharp_books_moved / row.total_books_moved
        sharp_alignment += (sharp_ratio - 0.35) * 45

    divergence = 50.0
    if row.sharp_percent is not None and row.public_percent is not None:
        diff = row.sharp_percent - row.public_percent
        divergence += diff * 0.55
        if diff >= 18:
            warnings.append("Sharp/public divergence supports market signal.")
        elif diff <= -18:
            warnings.append("Sharp/public divergence opposes selection.")

    if row.sharp_books_moved >= 3 and row.line_moves_last_30m >= 3:
        warnings.append("Clustered sharp-book movement detected.")

    return SteamDetectionOutput(
        steam_score=round(clamp(steam), 2),
        sharp_alignment_score=round(clamp(sharp_alignment), 2),
        public_divergence_score=round(clamp(divergence), 2),
        warnings=warnings,
    )
