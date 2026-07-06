# LUCA Production Repository — Phase 1

This is the first consolidated LUCA production repository.

## Phase 1 scope

Built as one deployable platform backbone:

- FastAPI application
- Universal core models
- Settings/configuration
- Provider interfaces
- Static dev providers
- Sport engine plugin registry
- Universal scoring and objective helpers
- Governance gates
- Unit authority
- Risk model
- Simulation service
- Workflow pipeline
- JSON + SQLite ledger repositories
- Results grading
- Calibration summary
- Replay shell
- Shadow mode shell
- Diagnostics and health API
- Publication/card formatter
- Test suite
- Railway/Docker/GitHub Action scaffolding

## Run locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Smoke test

```bash
pytest
curl "http://127.0.0.1:8000/health"
curl "http://127.0.0.1:8000/run-luca/nfl?date=2026-08-01&public=true"
```

## Deploy target

Railway can run:

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

Phase 2 should add live provider integrations and sport-specific feature mappers.
