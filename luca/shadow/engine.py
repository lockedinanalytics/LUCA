from __future__ import annotations
from pydantic import BaseModel
from luca.core.models import LucaRunResult

class ShadowComparison(BaseModel):
    production_version: str
    shadow_version: str
    production_recommendations: int
    shadow_recommendations: int
    agreement_rate: float | None
    notes: list[str]

def compare_shadow_run(production: LucaRunResult, shadow: LucaRunResult, production_version: str = "production", shadow_version: str = "shadow") -> ShadowComparison:
    prod = {p.selection for p in production.recommendations}
    shad = {p.selection for p in shadow.recommendations}
    union = prod | shad
    return ShadowComparison(
        production_version=production_version,
        shadow_version=shadow_version,
        production_recommendations=len(production.recommendations),
        shadow_recommendations=len(shadow.recommendations),
        agreement_rate=(len(prod & shad) / len(union)) if union else None,
        notes=["Shadow mode compares outputs without promoting shadow recommendations."],
    )
