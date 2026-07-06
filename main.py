from fastapi import FastAPI, Query
from luca.api.provider_routes import router as provider_router
from luca.api.intelligence_routes import router as intelligence_router
from luca.api.simulation_routes import router as simulation_router
from luca.api.mlb_intelligence_routes import router as mlb_intelligence_router
from luca.api.decision_routes import router as decision_router
from luca.api.mlb_pitching_routes import router as mlb_pitching_router
from luca.api.mlb_bullpen_routes import router as mlb_bullpen_router
from luca.api.mlb_offense_routes import router as mlb_offense_router
from luca.api.mlb_defense_routes import router as mlb_defense_router
from luca.api.mlb_environment_routes import router as mlb_environment_router
from luca.api.mlb_market_routes import router as mlb_market_router
from luca.api.validation_routes import router as validation_router
from luca.api.nfl_quarterback_routes import router as nfl_quarterback_router

from luca.calibration.engine import build_calibration_summary
from luca.config.settings import get_settings
from luca.core.models import Sport
from luca.database.json_repo import JsonLedgerRepository
from luca.database.sqlite_repo import SqliteLedgerRepository
from luca.diagnostics.health import build_system_health
from luca.ledger.storage import JsonLedgerStore
from luca.providers.factory import get_market_provider, get_schedule_provider
from luca.providers.odds.the_odds_api.provider import TheOddsApiMarketProvider
from luca.providers.static.provider import StaticMarketProvider, StaticScheduleProvider
from luca.publication.formatter import run_summary
from luca.run.orchestrator import run_luca_for_sport
from luca.simulation.engine import SimulationRequest, simulate_game
from luca.workflows.pipeline import LucaWorkflowPipeline, PipelineContext

settings = get_settings()
app = FastAPI(title=settings.app_name, version=settings.model_version)

@app.get("/")
async def root():
    return {"status": "ok", "service": "luca-udos", "version": settings.model_version}

@app.get("/health")
async def health():
    return build_system_health(settings.model_version)

@app.get("/providers/odds/status")
async def odds_status():
    return TheOddsApiMarketProvider().status().model_dump()

@app.get("/run-luca/{sport}")
async def run_luca(
    sport: Sport,
    date: str = Query(...),
    league: str | None = None,
    public: bool = False,
    schedule_provider: str | None = None,
    market_provider: str | None = None,
):
    result = run_luca_for_sport(
        sport,
        league or sport.value.upper(),
        date,
        get_schedule_provider(schedule_provider),
        get_market_provider(market_provider),
    )
    return run_summary(result) if public else result

@app.get("/workflow/run/{sport}")
async def workflow_run(
    sport: Sport,
    date: str = Query(...),
    league: str | None = None,
    write_ledger: bool = False,
    sqlite: bool = True,
    public: bool = False,
):
    repo = SqliteLedgerRepository(settings.sqlite_path) if sqlite else JsonLedgerRepository(settings.json_ledger_path)
    pipe = LucaWorkflowPipeline(get_schedule_provider(), get_market_provider(), repo)
    result = pipe.run(PipelineContext(sport=sport, league=league or sport.value.upper(), date=date, write_ledger=write_ledger))
    return run_summary(result) if public else result

@app.get("/calibration")
async def calibration(sqlite: bool = True):
    repo = SqliteLedgerRepository(settings.sqlite_path) if sqlite else None
    rows = repo.list_decisions() if repo else JsonLedgerStore(settings.json_ledger_path).list_all()
    return build_calibration_summary(rows)

@app.get("/simulate/sample")
async def simulate_sample(home_mean: float = 4.5, away_mean: float = 4.2, runs: int = 10000):
    return simulate_game(SimulationRequest(game_id="sample", runs=runs, mean_home=home_mean, mean_away=away_mean))
