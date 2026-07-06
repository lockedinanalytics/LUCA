from __future__ import annotations

from pydantic import BaseModel


class CompletenessReport(BaseModel):
    completeness: float
    missing: list[str]
    warnings: list[str]


def validate_required_fields(payload: dict, required: list[str]) -> CompletenessReport:
    missing = [field for field in required if payload.get(field) in {None, ""}]
    completeness = 1.0 - (len(missing) / len(required) if required else 0.0)
    warnings = []
    if completeness < 0.70:
        warnings.append("Data completeness below governance threshold.")
    return CompletenessReport(completeness=round(completeness, 3), missing=missing, warnings=warnings)
