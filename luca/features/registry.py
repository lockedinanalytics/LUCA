from __future__ import annotations
from typing import Dict, List, Optional
from pydantic import BaseModel

class FeatureDefinition(BaseModel):
    feature_id: str
    name: str
    sport: str
    engine: str
    description: str
    units: str = "score"
    update_frequency: str = "per_run"
    expected_direction: str = "higher_better"
    source: Optional[str] = None
    validation_status: str = "research"

FEATURES: Dict[str, FeatureDefinition] = {}

def register_feature(feature: FeatureDefinition) -> None:
    FEATURES[feature.feature_id] = feature

def list_features(sport: str | None = None, engine: str | None = None) -> List[FeatureDefinition]:
    rows = list(FEATURES.values())
    if sport:
        rows = [r for r in rows if r.sport == sport]
    if engine:
        rows = [r for r in rows if r.engine == engine]
    return rows

def load_default_features() -> None:
    defaults = [
        ("SP-001", "Four-Seam Fastball Velocity", "mlb", "starting_pitching", "Pitcher velocity signal"),
        ("SP-002", "Velocity Delta", "mlb", "starting_pitching", "Current velocity versus baseline"),
        ("RCP-001", "Expected Runs First Time Through", "mlb", "run_creation", "Lineup run creation first time through order"),
        ("BSI-001", "Bullpen Fatigue Score", "mlb", "bullpen", "Recent bullpen workload stress"),
        ("NFL-001", "QB Edge", "nfl", "quarterback", "Quarterback advantage score"),
        ("NFL-002", "OL/DL Edge", "nfl", "trenches", "Line of scrimmage advantage"),
        ("NCAAF-001", "Team Power Edge", "ncaaf", "team_power", "College team strength differential"),
        ("NBA-001", "Player Availability Edge", "nba", "availability", "Availability and rotation impact"),
        ("SOC-001", "xG Edge", "soccer", "expected_goals", "Expected goal differential"),
        ("SURV-001", "Weekly Survival Probability", "nfl", "survivor", "Current week survival probability"),
    ]
    for fid, name, sport, engine, desc in defaults:
        register_feature(FeatureDefinition(feature_id=fid, name=name, sport=sport, engine=engine, description=desc))

load_default_features()
