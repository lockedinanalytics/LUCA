from __future__ import annotations

from pydantic import BaseModel


class TeamAlias(BaseModel):
    canonical: str
    aliases: list[str]
    sport: str | None = None
    league: str | None = None
