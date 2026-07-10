from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


# ============================================================
# LUCA MLB Offense Intelligence Models
# Governance Authority Production Migration
# Phase 40 Cleanup
# ============================================================


class OffenseIntelligenceStatus(str, Enum):
    AVAILABLE = "available"
    PROJECTED = "projected"
    INCOMPLETE = "incomplete"
    UNAVAILABLE = "unavailable"


class LineupStatus(str, Enum):
    CONFIRMED = "confirmed"
    PROJECTED = "projected"
    PARTIAL = "partial"
    UNAVAILABLE = "unavailable"


class OffenseSide(str, Enum):
    HOME = "home"
    AWAY = "away"


class OffenseSourceType(str, Enum):
    OFFICIAL = "official"
    TRUSTED_PROJECTION = "trusted_projection"
    LUCA_PROJECTION = "luca_projection"
    NEUTRAL = "neutral_no_adjustment"
    UNKNOWN = "unknown"


class BatterProfile(BaseModel):
    player_id: int | str | None = None
    player_name: str | None = None
    batting_order: int | None = None
    position: str | None = None
    bats: str | None = None

    xwoba: float | None = None
    woba: float | None = None
    iso: float | None = None
    slugging: float | None = None
    on_base_percentage: float | None = None
    strikeout_rate: float | None = None
    walk_rate: float | None = None

    pitch_type_values: dict[str, float] = Field(default_factory=dict)
    platoon_splits: dict[str, float] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)


class TeamOffenseInput(BaseModel):
    team_id: int | str | None = None
    team_name: str
    side: OffenseSide

    lineup_status: LineupStatus = LineupStatus.UNAVAILABLE
    source_type: OffenseSourceType = OffenseSourceType.UNKNOWN
    source_name: str | None = None

    batters: list[BatterProfile] = Field(default_factory=list)

    team_xwoba: float | None = None
    team_woba: float | None = None
    team_iso: float | None = None
    team_slugging: float | None = None
    team_obp: float | None = None
    team_k_rate: float | None = None
    team_bb_rate: float | None = None

    recent_run_creation: float | None = None
    lineup_cohesion: float | None = None
    platoon_advantage_score: float | None = None
    pitch_type_matchup_score: float | None = None
    park_adjustment: float | None = None

    metadata: dict[str, Any] = Field(default_factory=dict)


class OffenseIntelligenceInput(BaseModel):
    game_id: str
    sport: str = "MLB"

    home_team: TeamOffenseInput
    away_team: TeamOffenseInput

    opposing_pitcher_context: dict[str, Any] = Field(default_factory=dict)
    park_context: dict[str, Any] = Field(default_factory=dict)
    weather_context: dict[str, Any] = Field(default_factory=dict)

    metadata: dict[str, Any] = Field(default_factory=dict)


class TeamOffenseIntelligence(BaseModel):
    team_name: str
    side: OffenseSide

    status: OffenseIntelligenceStatus
    lineup_status: LineupStatus
    source_type: OffenseSourceType
    source_name: str | None = None

    raw_score: float = 50.0
    adjusted_score: float = 50.0
    run_creation_projection: float = 50.0

    component_scores: dict[str, float] = Field(default_factory=dict)

    warnings: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class OffenseIntelligenceOutput(BaseModel):
    game_id: str
    sport: str = "MLB"

    status: OffenseIntelligenceStatus

    home_offense: TeamOffenseIntelligence
    away_offense: TeamOffenseIntelligence

    home_offense_rating: float = 50.0
    away_offense_rating: float = 50.0
    offense_edge: float = 0.0

    module_name: str = "mlb_offense_intelligence"
    module_version: str = "offense_models_v2_governance_cleanup"
    governance_role: str = "diagnostic_only"

    warnings: list[str] = Field(default_factory=list)
    blockers: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class OffenseHealth(BaseModel):
    status: str = "ok"
    module: str = "mlb_offense_intelligence"
    model_version: str = "offense_models_v2_governance_cleanup"
    governance_role: str = "diagnostic_only"
    production_notes: list[str] = Field(
        default_factory=lambda: [
            "Governance Score is the single certification authority.",
            "Upstream Presidential modules are diagnostic only and must not apply scoring penalties.",
            "Governance Authority is the production selection engine.",
            "Pipeline has been migrated to Governance Authority.",
            "Totals Authority v5 completed.",
        ]
    )
    metadata: dict[str, Any] = Field(default_factory=dict)
