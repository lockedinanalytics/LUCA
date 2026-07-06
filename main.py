from __future__ import annotations

from fastapi import FastAPI

from luca.calibration.engine import build_calibration_summary
from luca.ledger.storage import JsonLedgerStore

app = FastAPI(
    title="LUCA Universal Decision Operating System",
    description="Transferable LUCA build scaffold.",
    version="0.1.0",
)


@app.get("/")
async def root():
    return {
        "status": "ok",
        "service": "luca-udos",
        "version": "0.1.0",
        "routes": ["/health", "/calibration"],
    }


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "kernel": "operational",
        "sports": ["mlb", "nfl", "ncaaf", "nba", "nhl", "soccer", "golf", "tennis", "mma"],
    }


@app.get("/calibration")
async def calibration():
    store = JsonLedgerStore()
    return build_calibration_summary(store.list_all())
