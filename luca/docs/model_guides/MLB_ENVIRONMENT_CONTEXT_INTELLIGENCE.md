# MLB Environment & Context Intelligence - Epic 1E

## Purpose
Epic 1E adds the environment and game context layer for MLB.

## Components
- Weather Vector Scoring
- Park Physics
- Travel and Rest Context
- Umpire Profile
- Game Context
- Composite Environment Context Engine

## Output
The engine returns:
- weather_score
- park_score
- travel_score
- umpire_score
- context_score
- run_environment_modifier
- pitching_environment_modifier
- offensive_environment_modifier
- final_environment_score
- confidence
- warnings
- explainability

## Sample endpoints
- `/intelligence/mlb/environment/weather/sample`
- `/intelligence/mlb/environment/park/sample`
- `/intelligence/mlb/environment/travel/sample`
- `/intelligence/mlb/environment/umpire/sample`
- `/intelligence/mlb/environment/context/sample`
- `/intelligence/mlb/environment/environment-v2/sample`
