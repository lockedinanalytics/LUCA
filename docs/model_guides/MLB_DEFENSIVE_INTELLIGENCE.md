# MLB Defensive Intelligence - Epic 1D

## Purpose
Epic 1D upgrades CAM from a simple catcher modifier into a broader defensive intelligence engine.

## Components
- Catcher Availability Modifier v2
- Receiving and framing
- Blocking
- Throwing and pop time
- Pitcher-catcher fit
- Infield and outfield defensive support
- OAA/DRS-style conversion
- Baserunner advancement prevention
- Defensive Run Prevention Score

## Output
The engine returns:
- cam_score
- fielding_score
- baserunner_prevention_score
- contact_support_score
- defensive_run_prevention_score
- confidence
- warnings
- explainability

## Sample endpoints
- `/intelligence/mlb/defense/catcher/sample`
- `/intelligence/mlb/defense/fielding/sample`
- `/intelligence/mlb/defense/baserunner-prevention/sample`
- `/intelligence/mlb/defense/defense-v2/sample`
