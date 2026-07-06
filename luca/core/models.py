from __future__ import annotations
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class Sport(str, Enum):
    MLB = "mlb"; NFL = "nfl"; NCAAF = "ncaaf"; NBA = "nba"; NHL = "nhl"
    SOCCER = "soccer"; GOLF = "golf"; TENNIS = "tennis"; MMA = "mma"

class GovernanceStatus(str, Enum):
    APPROVED = "approved"; HOLD = "hold"; REJECTED = "rejected"; PASS = "pass"; AVOID = "avoid"

class PickCategory(str, Enum):
    PRESIDENTIAL = "presidential"; VICE_PRESIDENTIAL = "vice_presidential"; CABINET = "cabinet"
    BEST_TOTAL = "best_total"; SECONDARY_TOTAL = "secondary_total"; PROP = "prop"; CONTEST = "contest"
    LEAN = "lean"; PASS = "pass"; AVOID = "avoid"

class MarketType(str, Enum):
    MONEYLINE = "moneyline"; SPREAD = "spread"; TOTAL = "total"; TEAM_TOTAL = "team_total"
    PROP = "prop"; FUTURE = "future"; CONTEST = "contest"

class TeamGame(BaseModel):
    game_id: str
    sport: Sport
    league: str
    date: str
    away_team: str
    home_team: str
    start_time: Optional[str] = None
    venue: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class MarketLine(BaseModel):
    game_id: str
    market_type: MarketType
    selection: str
    book: Optional[str] = None
    open_odds: Optional[float] = None
    current_odds: Optional[float] = None
    close_odds: Optional[float] = None
    spread: Optional[float] = None
    total: Optional[float] = None
    timestamp: Optional[str] = None

class ModuleScores(BaseModel):
    scores: Dict[str, float] = Field(default_factory=dict)
    def get(self, key: str, default: float = 50.0) -> float:
        return float(self.scores.get(key, default))

class GameEvaluation(BaseModel):
    game: TeamGame
    projected_score: Optional[str] = None
    projected_margin: Optional[float] = None
    projected_total: Optional[float] = None
    moneyline_probability: Optional[float] = None
    spread_probability: Optional[float] = None
    total_probability: Optional[float] = None
    best_edge: Optional[float] = None
    risk_grade: str = "ungraded"
    variance_grade: str = "ungraded"
    module_scores: ModuleScores = Field(default_factory=ModuleScores)
    raw: Dict[str, Any] = Field(default_factory=dict)

class PickRecommendation(BaseModel):
    category: PickCategory
    sport: Sport
    league: str
    game_id: str
    market_type: MarketType
    selection: str
    odds: Optional[float] = None
    confidence: float
    units: float
    expected_value: Optional[float] = None
    luca_score: Optional[float] = None
    governance_status: GovernanceStatus
    publication_status: str = "internal"
    notes: List[str] = Field(default_factory=list)
    audit: Dict[str, Any] = Field(default_factory=dict)

class LucaRunResult(BaseModel):
    sport: Sport
    league: str
    date: str
    slate_size: int
    games_evaluated: int
    market_timestamp: Optional[str] = None
    data_completeness: float = 0.0
    model_version: str = "0.2.0"
    run_status: str = "ok"
    evaluations: List[GameEvaluation] = Field(default_factory=list)
    recommendations: List[PickRecommendation] = Field(default_factory=list)
    pass_list: List[Dict[str, Any]] = Field(default_factory=list)
