from __future__ import annotations

from fastapi import FastAPI

from luca.routes.api import router

app = FastAPI(
    title="LUCA Universal Decision Operating System",
    description="Transferable LUCA build scaffold.",
    version="0.6.0",
)

app.include_router(router)


@app.get("/")
async def root():
    return {
        "status": "ok",
        "service": "luca-udos",
        "version": "0.6.0",
        "routes": [
            "/health",
            "/features",
            "/calibration",
            "/run-luca/{sport}",
            "/workflow/run/{sport}",
            "/simulate/sample",
            "/freshness/sample",
            "/results/grade",
            "/survivor/sample",
        ],
    }
