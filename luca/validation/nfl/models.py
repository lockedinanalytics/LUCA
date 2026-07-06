from __future__ import annotations

from pydantic import BaseModel, Field

from luca.validation.replay.models import HistoricalDecision


class NflReplayInput(BaseModel):
    replay_id: str
    model_version: str
    decisions: list[HistoricalDecision] = Field(default_factory=list)


class NflMarketValidationSlice(BaseModel):
    market: str
    decisions: int
    wins: int
    losses: int
    pushes: int
    units: float
    roi: float | None
    avg_clv_delta: float | None
    brier_score: float | None


class NflValidationSummary(BaseModel):
    replay_id: str
    model_version: str
    total_decisions: int
    graded_decisions: int
    market_slices: list[NflMarketValidationSlice]
    calibration_bias: float | None
    overall_brier_score: float | None
    clv_health_score: float
    readiness_score: float
    promotion_ready: bool
    warnings: list[str] = Field(default_factory=list)


class NflPromotionGateInput(BaseModel):
    validation: NflValidationSummary
    min_decisions: int = 100
    max_abs_calibration_bias: float = 0.08
    min_roi: float = -0.02
    min_clv_health_score: float = 45.0
    min_readiness_score: float = 60.0


class NflPromotionGateOutput(BaseModel):
    approved: bool
    readiness_score: float
    failed_gates: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
