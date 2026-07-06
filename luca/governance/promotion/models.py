from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field


class PromotionRecord(BaseModel):
    promotion_id: str
    sport: str
    from_version: str
    to_version: str
    approved: bool
    readiness_score: float
    failed_gates: list[str] = Field(default_factory=list)
    approved_by: str = "LUCA Governance"
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    notes: list[str] = Field(default_factory=list)
