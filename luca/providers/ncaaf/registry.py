from __future__ import annotations

from luca.intelligence.ncaaf.foundation.models import NcaafTeamRegistryEntry


POWER_FOUR = {"ACC", "Big Ten", "Big 12", "SEC"}
GROUP_OF_FIVE = {"AAC", "C-USA", "MAC", "Mountain West", "Sun Belt"}


def classify_power_tier(conference: str, subdivision: str = "FBS") -> str:
    if subdivision.upper() == "FCS":
        return "FCS"
    if conference in POWER_FOUR:
        return "P4"
    if conference in GROUP_OF_FIVE:
        return "G5"
    return "Independent"


def build_registry_entry(team_id: str, school: str, conference: str, subdivision: str = "FBS", **kwargs) -> NcaafTeamRegistryEntry:
    return NcaafTeamRegistryEntry(
        team_id=team_id,
        school=school,
        conference=conference,
        subdivision=subdivision,
        power_tier=classify_power_tier(conference, subdivision),
        **kwargs,
    )


def sample_registry() -> list[NcaafTeamRegistryEntry]:
    return [
        build_registry_entry("uga", "Georgia", "SEC", nickname="Bulldogs", home_venue="Sanford Stadium", climate_region="humid"),
        build_registry_entry("osu", "Ohio State", "Big Ten", nickname="Buckeyes", home_venue="Ohio Stadium", climate_region="cold"),
        build_registry_entry("boise", "Boise State", "Mountain West", nickname="Broncos", home_venue="Albertsons Stadium", altitude_ft=2700, climate_region="mountain"),
        build_registry_entry("nd", "Notre Dame", "Independent", nickname="Fighting Irish", home_venue="Notre Dame Stadium", climate_region="cold"),
    ]
