from __future__ import annotations

from fastapi import APIRouter

from luca.core.models import Sport, TeamGame
from luca.intelligence.mlb.bsi import BullpenUsageInput, calculate_bsi
from luca.intelligence.mlb.rcp import RunCreationInput, calculate_rcp
from luca.intelligence.market.smi import MarketMovementInput, calculate_smi
from luca.intelligence.weather.engine import score_weather
from luca.providers.venues.resolver import VenueResolver
from luca.providers.weather.models import WeatherSnapshot

router = APIRouter(prefix="/intelligence", tags=["intelligence"])


@router.get("/venues/resolve")
async def resolve_venue(name: str | None = None, team: str | None = None):
    venue = VenueResolver().resolve(name, team)
    return venue.model_dump() if venue else {"available": False}


@router.get("/weather/score")
async def weather_score(
    game_id: str = "sample",
    temperature_f: float | None = None,
    wind_speed_mph: float | None = None,
    roof: str = "open",
):
    snapshot = WeatherSnapshot(
        game_id=game_id,
        available=True,
        temperature_f=temperature_f,
        wind_speed_mph=wind_speed_mph,
        source="manual_query",
    )
    return score_weather(snapshot, roof=roof).model_dump()


@router.get("/mlb/bsi/sample")
async def bsi_sample(total_pitches_yesterday: int = 45, total_pitches_last_3_days: int = 120, back_to_back_relievers: int = 2):
    return calculate_bsi(BullpenUsageInput(
        total_pitches_yesterday=total_pitches_yesterday,
        total_pitches_last_3_days=total_pitches_last_3_days,
        back_to_back_relievers=back_to_back_relievers,
    )).model_dump()


@router.get("/mlb/rcp/sample")
async def rcp_sample(top_order_score: float = 58, bottom_order_score: float = 52, pitcher_matchup_score: float = 55):
    return calculate_rcp(RunCreationInput(
        top_order_score=top_order_score,
        bottom_order_score=bottom_order_score,
        pitcher_matchup_score=pitcher_matchup_score,
    )).model_dump()


@router.get("/market/smi/sample")
async def smi_sample(opening_odds: float = -110, current_odds: float = -125, public_percent: float = 45, sharp_percent: float = 62):
    return calculate_smi(MarketMovementInput(
        opening_odds=opening_odds,
        current_odds=current_odds,
        public_percent=public_percent,
        sharp_percent=sharp_percent,
    )).model_dump()
