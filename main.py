from __future__ import annotations
from fastapi import FastAPI, Query
from luca.calibration.engine import build_calibration_summary
from luca.contests.circa_survivor.engine import SurvivorTeamOption, rank_survivor_options
from luca.core.models import Sport
from luca.database.json_repo import JsonLedgerRepository
from luca.diagnostics.health import build_system_health
from luca.features.registry import list_features
from luca.ledger.storage import JsonLedgerStore
from luca.providers.static.provider import StaticMarketProvider, StaticScheduleProvider
from luca.publication.formatter import run_summary
from luca.run.orchestrator import run_luca_for_sport
from luca.workflows.pipeline import LucaWorkflowPipeline, PipelineContext

app = FastAPI(title="LUCA Universal Decision Operating System", description="Transferable LUCA build scaffold.", version="0.4.0")

@app.get("/")
async def root():
    return {"status": "ok", "service": "luca-udos", "version": "0.4.0",
            "routes": ["/health", "/diagnostics/health", "/features", "/calibration", "/run-luca/{sport}", "/workflow/run/{sport}", "/survivor/sample"]}

@app.get("/health")
async def health():
    return {"status": "ok", "kernel": "operational",
            "sports": ["mlb", "nfl", "ncaaf", "nba", "nhl", "soccer", "golf", "tennis", "mma"]}

@app.get("/diagnostics/health")
async def diagnostics_health():
    return build_system_health().model_dump()

@app.get("/features")
async def features(sport: str | None = None, engine: str | None = None):
    return [f.model_dump() for f in list_features(sport=sport, engine=engine)]

@app.get("/calibration")
async def calibration():
    return build_calibration_summary(JsonLedgerStore().list_all())

@app.get("/run-luca/{sport}")
async def run_luca(sport: Sport, date: str = Query(...), league: str | None = None, public: bool = False):
    result = run_luca_for_sport(sport, league or sport.value.upper(), date, StaticScheduleProvider(), StaticMarketProvider())
    return run_summary(result) if public else result

@app.get("/workflow/run/{sport}")
async def workflow_run(sport: Sport, date: str = Query(...), league: str | None = None, write_ledger: bool = False, public: bool = False):
    pipeline = LucaWorkflowPipeline(StaticScheduleProvider(), StaticMarketProvider(), JsonLedgerRepository())
    result = pipeline.run(PipelineContext(sport=sport, league=league or sport.value.upper(), date=date, write_ledger=write_ledger))
    return run_summary(result) if public else result

@app.get("/survivor/sample")
async def survivor_sample():
    options = [
        SurvivorTeamOption(team="BUF", win_probability=0.78, future_value=88, ownership_projection=32, scarcity_score=70, schedule_path_value=82, risk_stability=76),
        SurvivorTeamOption(team="KC", win_probability=0.80, future_value=95, ownership_projection=44, scarcity_score=60, schedule_path_value=90, risk_stability=78),
        SurvivorTeamOption(team="MIN", win_probability=0.70, future_value=62, ownership_projection=12, scarcity_score=82, schedule_path_value=68, risk_stability=70),
    ]
    return [row.model_dump() for row in rank_survivor_options(options)]
