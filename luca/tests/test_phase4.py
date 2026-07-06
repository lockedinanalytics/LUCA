from luca.providers.venues.resolver import VenueResolver
from luca.providers.weather.models import WeatherSnapshot
from luca.intelligence.weather.engine import score_weather
from luca.intelligence.mlb.bsi import BullpenUsageInput, calculate_bsi
from luca.intelligence.mlb.rcp import RunCreationInput, calculate_rcp
from luca.intelligence.market.smi import MarketMovementInput, calculate_smi


def test_venue_resolver():
    venue = VenueResolver().resolve(team="Los Angeles Dodgers")
    assert venue is not None
    assert venue.name == "Dodger Stadium"


def test_weather_score():
    impact = score_weather(WeatherSnapshot(game_id="x", available=True, temperature_f=88, wind_speed_mph=12))
    assert impact.weather_score >= 50


def test_bsi():
    row = calculate_bsi(BullpenUsageInput(total_pitches_yesterday=45, total_pitches_last_3_days=120, back_to_back_relievers=2))
    assert 0 <= row.final_bsi <= 100


def test_rcp():
    row = calculate_rcp(RunCreationInput(top_order_score=60, bottom_order_score=52, pitcher_matchup_score=55))
    assert row.projected_runs > 0


def test_smi():
    row = calculate_smi(MarketMovementInput(opening_odds=-110, current_odds=-125, public_percent=45, sharp_percent=62))
    assert row.smi_score >= 50
