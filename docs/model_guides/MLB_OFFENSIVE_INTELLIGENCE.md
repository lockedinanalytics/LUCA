# MLB Offensive Intelligence - Epic 1C

## Purpose
Epic 1C upgrades Run Creation Projection into hitter-level offensive intelligence.

## Components
- Hitter Quality
- Lineup Chain Strength
- On-Base Chain
- Power Cascade
- Strikeout Cluster Risk
- Platoon Fit
- Bench / Pinch-Hit Adjustment
- Run Creation Projection v2

## Output
The engine returns:
- lineup_chain_score
- platoon_score
- starter_matchup_score
- bullpen_matchup_score
- run_environment_score
- projected_runs
- explosive_inning_probability
- final_rcp_score
- confidence
- warnings
- explainability

## Sample endpoints
- `/intelligence/mlb/offense/hitter/sample`
- `/intelligence/mlb/offense/lineup-chain/sample`
- `/intelligence/mlb/offense/platoon/sample`
- `/intelligence/mlb/offense/rcp-v2/sample`
