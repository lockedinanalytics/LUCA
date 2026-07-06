# LUCA Universal Decision Operating System — Repo Conversion v2

This version upgrades the LUCA scaffold from interface-only to formula-ready.

## Added in v2
- Universal feature registry
- Universal analytics engine formulas
- Objective engine thresholds
- Governance gates
- Sport formula configuration
- Publication formatter
- Expanded FastAPI routes
- Basic tests

## Run locally
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## v3 additions
- Run orchestrator
- Static providers
- /run-luca/{sport}
- Circa Survivor scoring

## v4 additions
- Workflow pipeline
- Database abstraction
- Diagnostics health endpoint
- Replay shell
- Shadow mode shell
- Structured logging
- Optional ledger write in workflow route
