# MLB Market Intelligence - Epic 1F

## Purpose
Epic 1F upgrades SMI into a full market intelligence engine.

## Components
- Line Movement
- Steam Detection
- Book Disagreement
- Implied-Probability CLV
- Market Contradiction
- Liquidity Confidence
- Smart Money Index v2

## Output
The engine returns:
- line_movement_score
- steam_score
- book_disagreement_score
- clv_score
- contradiction_score
- liquidity_confidence
- final_smi_score
- confidence
- warnings
- explainability

## Sample endpoints
- `/intelligence/mlb/market/line-movement/sample`
- `/intelligence/mlb/market/steam/sample`
- `/intelligence/mlb/market/book-disagreement/sample`
- `/intelligence/mlb/market/clv/sample`
- `/intelligence/mlb/market/contradiction/sample`
- `/intelligence/mlb/market/smi-v2/sample`
