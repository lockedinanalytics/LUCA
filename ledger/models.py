from __future__ import annotations
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field

class LedgerDecision(BaseModel):
    decision_id: str
    game_id: str
    date: str
    sport: str
    league: str
    category: str
    market: str
    selection: str
    odds: Optional[float]=None
    units: float=0.0
    confidence: float=0.0
    luca_score: Optional[float]=None
    expected_value: Optional[float]=None
    result: Optional[str]=None
    units_won_lost: Optional[float]=None
    final_score: Optional[str]=None
    closing_odds: Optional[float]=None
    clv: Optional[float]=None
    module_snapshot: Dict[str, Any]=Field(default_factory=dict)
    governance_snapshot: Dict[str, Any]=Field(default_factory=dict)
    audit_status: str="pending"
