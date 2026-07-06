from __future__ import annotations

from pydantic import BaseModel, Field


class BookLineInput(BaseModel):
    book: str
    odds: float | None = None
    point: float | None = None
    timestamp: str | None = None
    is_sharp_book: bool = False
    liquidity_score: float = 50.0


class MarketTimelineInput(BaseModel):
    market: str = "moneyline"
    selection: str = "unknown"
    opening_odds: float | None = None
    current_odds: float | None = None
    closing_odds: float | None = None
    opening_point: float | None = None
    current_point: float | None = None
    closing_point: float | None = None
    minutes_since_open: float | None = None
    minutes_to_start: float | None = None
    books: list[BookLineInput] = Field(default_factory=list)


class LineMovementOutput(BaseModel):
    odds_movement: float | None
    point_movement: float | None
    movement_velocity_score: float
    directional_strength_score: float
    late_move_score: float
    warnings: list[str] = Field(default_factory=list)


class SteamDetectionInput(BaseModel):
    line_moves_last_30m: int = 0
    sharp_books_moved: int = 0
    total_books_moved: int = 0
    average_move_size: float = 0.0
    public_percent: float | None = None
    sharp_percent: float | None = None


class SteamDetectionOutput(BaseModel):
    steam_score: float
    sharp_alignment_score: float
    public_divergence_score: float
    warnings: list[str] = Field(default_factory=list)


class BookDisagreementOutput(BaseModel):
    disagreement_score: float
    best_price_edge_score: float
    consensus_quality_score: float
    liquidity_score: float
    warnings: list[str] = Field(default_factory=list)


class ClvInput(BaseModel):
    published_odds: float | None = None
    closing_odds: float | None = None
    projected_probability: float | None = None


class ClvOutput(BaseModel):
    clv_implied_probability_delta: float | None
    beat_close: bool | None
    clv_score: float
    warnings: list[str] = Field(default_factory=list)


class MarketContradictionInput(BaseModel):
    model_edge_score: float = 50.0
    market_support_score: float = 50.0
    public_percent: float | None = None
    sharp_percent: float | None = None
    reverse_line_movement: bool = False


class MarketContradictionOutput(BaseModel):
    contradiction_score: float
    agreement_score: float
    warnings: list[str] = Field(default_factory=list)


class SmartMoneyV2Input(BaseModel):
    timeline: MarketTimelineInput = Field(default_factory=MarketTimelineInput)
    steam: SteamDetectionInput = Field(default_factory=SteamDetectionInput)
    clv: ClvInput = Field(default_factory=ClvInput)
    contradiction: MarketContradictionInput = Field(default_factory=MarketContradictionInput)


class SmartMoneyV2Output(BaseModel):
    line_movement_score: float
    steam_score: float
    book_disagreement_score: float
    clv_score: float
    contradiction_score: float
    liquidity_confidence: float
    final_smi_score: float
    confidence: float
    warnings: list[str] = Field(default_factory=list)
    explainability: dict[str, float] = Field(default_factory=dict)
