from __future__ import annotations

from fastapi import FastAPI, Query

from luca.calibration.engine import build_calibration_summary
from luca.contests.circa_survivor.engine import SurvivorTeamOption, rank_survivor_options
from luca.core.models import Sport
from luca.features.registry import list_features
from luca.ledger.storage import JsonLedgerStore
from luca.providers.static.provider import StaticMarketProvider, StaticScheduleProvider
from luca.publication.formatter import run_summary
from luca.run.orchestrator import run_luca_for_sport

app = FastAPI(
    title="LUCA Universal Decision Operating System",
    description="Transferable LUCA build scaffold.",
    version="0.3.0",
)


@app.get("/")
async def root():
    return {
        "status": "ok",
        "service": "luca-udos",
        "version": "0.3.0",
        "routes": ["/health", "/features", "/calibration", "/run-luca/{sport}", "/survivor/sample"],
    }


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "kernel": "operational",
        "sports": ["mlb", "nfl", "ncaaf", "nba", "nhl", "soccer", "golf", "tennis", "mma"],
        "layers": ["core", "features", "analytics", "objectives", "governance", "ledger", "calibration", "run"],
    }


@app.get("/features")
async def features(sport: str | None = None, engine: str | None = None):
    return [f.model_dump() for f in list_features(sport=sport, engine=engine)]


@app.get("/calibration")
async def calibration():
    store = JsonLedgerStore()
    return build_calibration_summary(store.list_all())


@app.get("/run-luca/{sport}")
async def run_luca(
    sport: Sport,
    date: str = Query(...),
    league: str | None = None,
    public: bool = False,
):
    result = run_luca_for_sport(
        sport=sport,
        league=league or sport.value.upper(),
        date=date,
        schedule_provider=StaticScheduleProvider(),
        market_provider=StaticMarketProvider(),
    )
    return run_summary(result) if public else result


@app.get("/survivor/sample")
async def survivor_sample():
    options = [
        SurvivorTeamOption(team="BUF", win_probability=0.78, future_value=88, ownership_projection=32, scarcity_score=70, schedule_path_value=82, risk_stability=76),
        SurvivorTeamOption(team="KC", win_probability=0.80, future_value=95, ownership_projection=44, scarcity_score=60, schedule_path_value=90, risk_stability=78),
        SurvivorTeamOption(team="MIN", win_probability=0.70, future_value=62, ownership_projection=12, scarcity_score=82, schedule_path_value=68, risk_stability=70),
    ]
    return [row.model_dump() for row in rank_survivor_options(options)]
