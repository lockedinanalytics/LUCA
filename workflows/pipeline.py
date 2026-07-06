from dataclasses import dataclass
from luca.core.models import LucaRunResult, Sport
from luca.database.base import LedgerRepository
from luca.ledger.models import LedgerDecision
from luca.providers.base import MarketProvider, ScheduleProvider
from luca.run.orchestrator import run_luca_for_sport

@dataclass
class PipelineContext:
    sport: Sport
    league: str
    date: str
    write_ledger: bool=False

class LucaWorkflowPipeline:
    def __init__(self, schedule_provider: ScheduleProvider, market_provider: MarketProvider, ledger_repository: LedgerRepository|None=None):
        self.schedule_provider=schedule_provider; self.market_provider=market_provider; self.ledger_repository=ledger_repository
    def run(self, context: PipelineContext) -> LucaRunResult:
        result=run_luca_for_sport(context.sport, context.league, context.date, self.schedule_provider, self.market_provider)
        if context.write_ledger and self.ledger_repository: self.ledger_repository.add_many(self._rows(result))
        return result
    def _rows(self, result: LucaRunResult) -> list[LedgerDecision]:
        return [LedgerDecision(decision_id=f"{result.sport.value}-{result.date}-{i}", game_id=p.game_id, date=result.date, sport=result.sport.value, league=result.league, category=p.category.value, market=p.market_type.value, selection=p.selection, odds=p.odds, units=p.units, confidence=p.confidence, luca_score=p.luca_score, expected_value=p.expected_value, module_snapshot=p.audit.get("modules",{}), governance_snapshot={"status":p.governance_status.value}) for i,p in enumerate(result.recommendations,1)]
