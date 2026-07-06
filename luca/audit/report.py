from __future__ import annotations

from pydantic import BaseModel

from luca.core.models import LucaRunResult


class AuditReport(BaseModel):
    sport: str
    league: str
    date: str
    games_evaluated: int
    recommendations: int
    pass_count: int
    data_completeness: float
    warnings: list[str]


def build_audit_report(result: LucaRunResult) -> AuditReport:
    warnings: list[str] = []
    if result.data_completeness < 0.70:
        warnings.append("Data completeness below governance threshold.")
    if not result.recommendations:
        warnings.append("No approved recommendations.")

    return AuditReport(
        sport=result.sport.value,
        league=result.league,
        date=result.date,
        games_evaluated=result.games_evaluated,
        recommendations=len(result.recommendations),
        pass_count=len(result.pass_list),
        data_completeness=result.data_completeness,
        warnings=warnings,
    )
