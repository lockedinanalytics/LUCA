# Phase 4 Status

## Added
- MLB venue coordinate seed data.
- Venue resolver.
- Open-Meteo weather provider implementation shell.
- Weather scoring engine.
- MLB boxscore feature extraction.
- MLB lineup snapshot extraction.
- MLB Bullpen Stress Index implementation.
- MLB Run Creation Projection implementation.
- Smart Money Index implementation.
- JSON market snapshot store.
- Manual officials provider shell.
- MLB feature mapper now calls BSI, RCP, and SMI engines.
- Intelligence API routes.

## API added
- `/intelligence/venues/resolve`
- `/intelligence/weather/score`
- `/intelligence/mlb/bsi/sample`
- `/intelligence/mlb/rcp/sample`
- `/intelligence/market/smi/sample`

## Next Phase
- Connect live MLB boxscore extraction to workflow.
- Add probable pitcher feature scoring.
- Add lineup quality scoring.
- Add weather into workflow context.
- Add market snapshot persistence during runs.
