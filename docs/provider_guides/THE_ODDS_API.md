# The Odds API Provider Guide

## Secret handling

Never hard-code the Odds API key.

Local `.env`:

```env
ODDS_API_KEY=your_key_here
ALLOW_LIVE_NETWORK_CALLS=true
MARKET_PROVIDER=the_odds_api
```

Railway Variables:

```env
ODDS_API_KEY=<your key>
ALLOW_LIVE_NETWORK_CALLS=true
MARKET_PROVIDER=the_odds_api
```

## Status endpoint

```bash
curl http://localhost:8000/providers/odds/status
```

The key is masked in output.

## Live run example

```bash
curl "http://localhost:8000/run-luca/mlb?date=2026-07-04&market_provider=the_odds_api&schedule_provider=mlb_stats_api"
```

## Supported sport-key defaults

- MLB -> baseball_mlb
- NFL -> americanfootball_nfl
- NCAAF -> americanfootball_ncaaf
- NBA -> basketball_nba
- NHL -> icehockey_nhl
- Soccer default -> soccer_epl
- MMA -> mma_mixed_martial_arts

Phase 3 should add alias matching and multi-league soccer support.
