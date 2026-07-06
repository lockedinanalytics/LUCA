# MLB Pitching Intelligence - Epic 1A

## Purpose
Epic 1A upgrades MLB Starting Pitcher Intelligence from a single starter score into a multi-component production engine.

## Components
- Pitch Arsenal
- Command
- Contact Management
- Fatigue
- Matchup

## Output
The engine returns:
- arsenal_score
- command_score
- contact_score
- fatigue_score
- matchup_score
- final_sp_score
- confidence
- warnings
- explainability

## Production Standard
This engine is designed to be fed by Statcast, MLB Stats API, manual override files, or historical replay datasets.

## Sample endpoints
- `/intelligence/mlb/pitching/arsenal/sample`
- `/intelligence/mlb/pitching/command/sample`
- `/intelligence/mlb/pitching/contact/sample`
- `/intelligence/mlb/pitching/fatigue/sample`
- `/intelligence/mlb/pitching/matchup/sample`
- `/intelligence/mlb/pitching/starter/sample`
