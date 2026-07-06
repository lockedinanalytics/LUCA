# Phase 2 Status

## Added
- Secure environment variable support for ODDS_API_KEY.
- The Odds API client, mapper, and provider.
- Provider factory for static/live providers.
- MLB Stats API schedule provider shell.
- Sport feature mapper interface.
- MLB feature mapper shell.
- Default feature mapper.
- Provider status endpoint.
- .env.example.
- Provider documentation.

## Live data safety
Live network calls are disabled by default.

To enable:
```env
ALLOW_LIVE_NETWORK_CALLS=true
```

## Next phase
- Alias resolver for team names across providers.
- Odds event matching reliability improvements.
- MLB boxscore, probable pitcher, lineup, bullpen, and weather provider mapping.
- NFL/NCAAF schedule provider integrations.
- Soccer league key routing.
