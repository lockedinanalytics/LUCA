from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict
from luca.core.models import LucaRunResult, Sport
from luca.database.base import LedgerRepository
from luca.ledger.models import LedgerDecision
from luca.logging.logger import get_logger
from luca.providers.base import MarketProvider, ScheduleProvider
from luca.run.orchestrator import run_luca_for_sport

@dataclass
class PipelineContext:
    sport: Sport
    league: str
    date: str
    write_ledger: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

class LucaWorkflowPipeline:
    def __init__(self, schedule_provider: ScheduleProvider, market_provider: MarketProvider, ledger_repository: LedgerRepository | None = None):
        self.schedule_provider = schedule_provider
        self.market_provider = market_provider
        self.ledger_repository = ledger_repository
        self.logger = get_logger("luca.workflow")

    def run(self, context: PipelineContext) -> LucaRunResult:
        self.logger.info("Starting LUCA workflow: %s %s %s", context.sport.value, context.league, context.date)
        result = run_luca_for_sport(context.sport, context.league, context.date, self.schedule_provider, self.market_provider)
        if context.write_ledger and self.ledger_repository:
            rows = self._recommendations_to_ledger(result)
            self.ledger_repository.add_many(rows)
            self.logger.info("Ledger rows written: %s", len(rows))
        return result

    def _recommendations_to_ledger(self, result: LucaRunResult) -> list[LedgerDecision]:
        rows: list[LedgerDecision] = []
        for idx, pick in enumerate(result.recommendations, start=1):
            rows.append(LedgerDecision(
                decision_id=f"{result.sport.value}-{result.date}-{idx}",
                game_id=pick.game_id,
                date=result.date,
                sport=result.sport.value,
                league=result.league,
                category=pick.category.value,
                market=pick.market_type.value,
                selection=pick.selection,
                odds=pick.odds,
                units=pick.units,
                confidence=pick.confidence,
                luca_score=pick.luca_score,
                expected_value=pick.expected_value,
                module_snapshot=pick.audit.get("modules", {}),
                governance_snapshot={"status": pick.governance_status.value},
            ))
        return rows
