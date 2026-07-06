from __future__ import annotations

from pydantic import BaseModel, Field


class NcaafTeamRegistryEntry(BaseModel):
    team_id: str
    school: str
    nickname: str | None = None
    conference: str = "Independent"
    subdivision: str = "FBS"
    power_tier: str = "G5"
    home_venue: str | None = None
    altitude_ft: float = 0.0
    climate_region: str = "neutral"


class NcaafGameKey(BaseModel):
    season: int
    week: int
    game_id: str
    home_team_id: str
    away_team_id: str
    neutral_site: bool = False
    conference_game: bool = False


class RecruitingProfileInput(BaseModel):
    recruiting_composite_score: float = 50.0
    blue_chip_ratio: float = 0.0
    avg_star_rating: float | None = None
    recruiting_momentum_score: float = 50.0
    position_group_depth_score: float = 50.0


class ReturningProductionInput(BaseModel):
    offensive_returning_production_pct: float = 50.0
    defensive_returning_production_pct: float = 50.0
    returning_starters_offense: int = 5
    returning_starters_defense: int = 5
    returning_qb_experience_score: float = 50.0
    offensive_line_continuity_score: float = 50.0


class TransferPortalInput(BaseModel):
    transfer_gain_score: float = 50.0
    transfer_loss_score: float = 50.0
    quarterback_transfer_score: float = 50.0
    defensive_transfer_score: float = 50.0
    portal_volatility_score: float = 50.0


class CoachingContinuityInput(BaseModel):
    head_coach_continuity_score: float = 50.0
    offensive_coordinator_continuity_score: float = 50.0
    defensive_coordinator_continuity_score: float = 50.0
    scheme_stability_score: float = 50.0
    staff_turnover_penalty: float = 0.0
    historical_system_performance_score: float = 50.0


class NcaafFoundationInput(BaseModel):
    recruiting: RecruitingProfileInput = Field(default_factory=RecruitingProfileInput)
    returning_production: ReturningProductionInput = Field(default_factory=ReturningProductionInput)
    transfer_portal: TransferPortalInput = Field(default_factory=TransferPortalInput)
    coaching: CoachingContinuityInput = Field(default_factory=CoachingContinuityInput)
    home_field_score: float = 50.0
    travel_burden_score: float = 50.0
    altitude_adaptation_score: float = 50.0
    climate_adaptation_score: float = 50.0


class NcaafFoundationOutput(BaseModel):
    roster_talent_score: float
    returning_production_score: float
    transfer_portal_score: float
    coaching_continuity_score: float
    program_strength_score: float
    volatility_score: float
    final_foundation_score: float
    confidence: float
    warnings: list[str] = Field(default_factory=list)
    explainability: dict[str, float] = Field(default_factory=dict)
