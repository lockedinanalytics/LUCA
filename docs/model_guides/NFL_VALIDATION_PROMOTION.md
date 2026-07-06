# NFL Validation, Calibration & Promotion Pipeline - Epic 2F

## Purpose
Epic 2F adds NFL-specific validation and governance promotion checks.

## Components
- NFL replay input
- NFL validation summary
- Market validation slices
- CLV health scoring
- Calibration and Brier reporting
- Promotion gates
- Promotion records

## Output
The engine returns:
- market_slices
- calibration_bias
- overall_brier_score
- clv_health_score
- readiness_score
- promotion_ready
- warnings

## Sample endpoints
- `/validation/nfl/summary/sample`
- `/validation/nfl/promotion/sample`
