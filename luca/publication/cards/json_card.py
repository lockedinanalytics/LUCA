from __future__ import annotations

from pydantic import BaseModel

from luca.core.models import LucaRunResult


class PublicCard(BaseModel):
    title: str
    sport: str
    league: str
    date: str
    picks: list[dict]
    footer: str = "Please bet responsibly. If you or someone you know has a gambling problem, call 1-800-GAMBLER."


def build_public_card(result: LucaRunResult, title: str | None = None) -> PublicCard:
    picks = [
        {
            "category": pick.category.value,
            "selection": pick.selection,
            "confidence": round(pick.confidence, 1),
            "units": pick.units,
        }
        for pick in result.recommendations
    ]
    return PublicCard(
        title=title or f"{result.league} Official Card",
        sport=result.sport.value,
        league=result.league,
        date=result.date,
        picks=picks,
    )
