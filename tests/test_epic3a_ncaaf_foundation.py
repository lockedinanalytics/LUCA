from luca.intelligence.ncaaf.foundation.engine import calculate_ncaaf_foundation
from luca.intelligence.ncaaf.foundation.models import NcaafFoundationInput, RecruitingProfileInput, ReturningProductionInput
from luca.providers.ncaaf.registry import classify_power_tier, sample_registry
from luca.providers.ncaaf.schedule import StaticNcaafScheduleProvider


def test_power_tier_classification():
    assert classify_power_tier("SEC") == "P4"
    assert classify_power_tier("Mountain West") == "G5"
    assert classify_power_tier("Big Sky", "FCS") == "FCS"


def test_registry_sample():
    rows = sample_registry()
    assert len(rows) >= 1
    assert rows[0].team_id


def test_schedule_provider():
    rows = StaticNcaafScheduleProvider().get_games(2026, 1)
    assert len(rows) >= 1
    assert rows[0].season == 2026


def test_foundation_engine_bounds():
    result = calculate_ncaaf_foundation(NcaafFoundationInput(
        recruiting=RecruitingProfileInput(recruiting_composite_score=72, blue_chip_ratio=0.58, avg_star_rating=3.9),
        returning_production=ReturningProductionInput(offensive_returning_production_pct=68, defensive_returning_production_pct=61),
    ))
    assert 0 <= result.final_foundation_score <= 100
    assert result.confidence > 0
