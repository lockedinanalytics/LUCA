from __future__ import annotations

from fastapi import APIRouter

from luca.providers.aliases.resolver import TeamAliasResolver
from luca.providers.odds.the_odds_api.provider import TheOddsApiMarketProvider

router = APIRouter(prefix="/providers", tags=["providers"])


@router.get("/odds/status")
async def odds_status():
    return TheOddsApiMarketProvider().status().model_dump()


@router.get("/aliases/resolve")
async def resolve_alias(name: str, sport: str | None = None, league: str | None = None):
    resolver = TeamAliasResolver()
    return {"input": name, "canonical": resolver.canonicalize(name, sport=sport, league=league)}
