from __future__ import annotations

from fastapi import APIRouter, Query

from luca.audit.report import build_audit_report
from luca.calibration.engine import build_calibration_summary
from luca.contests.circa_survivor.engine import SurvivorTeamOption, rank_survivor_options
from luca.core.models import Sport
from luca.database.json_repo import JsonLedgerRepository
from luca.database.sqlite_repo import SqliteLedgerRepository
from luca.diagnostics.health import build_system_health
from luca.features.registry import list_features
from luca.ledger.storage import JsonLedgerStore
from luca.providers.freshness.models import freshness_report
from luca.providers.static.provider import StaticMarketProvider, StaticScheduleProvider
from luca.publication.formatter import run_summary
from luca.publication.cards.json_card import build_public_card
from luca.results.grader import FinalResult
from luca.results.service import grade_game_decisions
from luca.run.orchestrator import run_luca_for_sport
from luca.simulation.engine import simulate_game
from luca.simulation.models import SimulationRequest
from luca.workflows.pipeline import LucaWorkflowPipeline, PipelineContext

router = APIRouter()


@router.get("/health")
async def health():
    return build_system_health(version="0.6.0").model_dump()


@router.get("/features")
async def features(sport: str | None = None, engine: str | None = None):
    return [f.model_dump() for f in list_features(sport=sport, engine=engine)]


@router.get("/calibration")
async def calibration(use_sqlite: bool = False):
    if use_sqlite:
        return build_calibration_summary(SqliteLedgerRepository().list_decisions())
    return build_calibration_summary(JsonLedgerStore().list_all())


@router.get("/run-luca/{sport}")
async def run_luca(sport: Sport, date: str = Query(...), league: str | None = None, public: bool = False, audit: bool = False):
    result = run_luca_for_sport(
        sport=sport,
        league=league or sport.value.upper(),
        date=date,
        schedule_provider=StaticScheduleProvider(),
        market_provider=StaticMarketProvider(),
    )
    if audit:
        return build_audit_report(result).model_dump()
    return run_summary(result) if public else result


@router.get("/workflow/run/{sport}")
async def workflow_run(
    sport: Sport,
    date: str = Query(...),
    league: str | None = None,
    write_ledger: bool = False,
    sqlite: bool = False,
    public: bool = False,
):
    repo = SqliteLedgerRepository() if sqlite else JsonLedgerRepository()
    pipeline = LucaWorkflowPipeline(
        schedule_provider=StaticScheduleProvider(),
        market_provider=StaticMarketProvider(),
        ledger_repository=repo,
    )
    result = pipeline.run(PipelineContext(sport=sport, league=league or sport.value.upper(), date=date, write_ledger=write_ledger))
    return run_summary(result) if public else result


@router.get("/simulate/sample")
async def simulate_sample(home_mean: float = 4.5, away_mean: float = 4.2, runs: int = 10000):
    return simulate_game(SimulationRequest(game_id="sample", mean_home=home_mean, mean_away=away_mean, runs=runs)).model_dump()


@router.get("/freshness/sample")
async def freshness_sample():
    return freshness_report(provider="static", last_updated_utc=None, max_age_seconds=300).model_dump()


@router.post("/results/grade")
async def grade_results(final: FinalResult, sqlite: bool = False):
    repo = SqliteLedgerRepository() if sqlite else JsonLedgerRepository()
    return [row.model_dump() for row in grade_game_decisions(repo, final)]


@router.get("/survivor/sample")
async def survivor_sample():
    options = [
        SurvivorTeamOption(team="BUF", win_probability=0.78, future_value=88, ownership_projection=32, scarcity_score=70, schedule_path_value=82, risk_stability=76),
        SurvivorTeamOption(team="KC", win_probability=0.80, future_value=95, ownership_projection=44, scarcity_score=60, schedule_path_value=90, risk_stability=78),
        SurvivorTeamOption(team="MIN", win_probability=0.70, future_value=62, ownership_projection=12, scarcity_score=82, schedule_path_value=68, risk_stability=70),
    ]
    return [row.model_dump() for row in rank_survivor_options(options)]


@router.get("/card/{sport}")
async def public_card(sport: Sport, date: str = Query(...), league: str | None = None):
    result = run_luca_for_sport(
        sport=sport,
        league=league or sport.value.upper(),
        date=date,
        schedule_provider=StaticScheduleProvider(),
        market_provider=StaticMarketProvider(),
    )
    return build_public_card(result).model_dump()
