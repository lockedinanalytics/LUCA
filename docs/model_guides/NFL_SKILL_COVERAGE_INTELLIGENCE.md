# NFL Skill Position & Coverage Intelligence - Epic 2C

## Purpose
Epic 2C introduces NFL skill-position and coverage matchup intelligence.

## Components
- Receiver Unit
- Tight End
- Running Back
- Coverage Unit
- Skill/Coverage Matchup Engine

## Output
The engine returns:
- receiver_score
- tight_end_score
- running_back_score
- coverage_score
- wr_cb_matchup_score
- te_matchup_score
- rb_matchup_score
- explosive_pass_projection
- possession_chain_score
- red_zone_skill_score
- final_skill_coverage_score
- confidence
- warnings
- explainability

## Sample endpoints
- `/intelligence/nfl/skill-coverage/receivers/sample`
- `/intelligence/nfl/skill-coverage/coverage/sample`
- `/intelligence/nfl/skill-coverage/matchup/sample`
