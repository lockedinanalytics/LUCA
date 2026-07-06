from __future__ import annotations

from luca.intelligence.market.v2.models import LineMovementOutput, MarketTimelineInput
from luca.intelligence.market.v2.utils import clamp, implied_probability_delta


def score_line_movement(row: MarketTimelineInput) -> LineMovementOutput:
    warnings: list[str] = []

    odds_move = None
    if row.opening_odds is not None and row.current_odds is not None:
        odds_move = row.current_odds - row.opening_odds

    point_move = None
    if row.opening_point is not None and row.current_point is not None:
        point_move = row.current_point - row.opening_point

    implied_delta = implied_probability_delta(row.opening_odds, row.current_odds)
    directional = 50.0
    if implied_delta is not None:
        directional += implied_delta * 650
        if abs(implied_delta) >= 0.025:
            warnings.append("Material implied-probability movement detected.")

    movement_magnitude = 0.0
    if odds_move is not None:
        movement_magnitude += abs(odds_move) * 0.35
    if point_move is not None:
        movement_magnitude += abs(point_move) * 7.0

    velocity = 50.0 + movement_magnitude
    if row.minutes_since_open and row.minutes_since_open > 0:
        velocity += min(15, movement_magnitude / max(1, row.minutes_since_open / 60))

    late = 50.0
    if row.minutes_to_start is not None and row.minutes_to_start <= 120:
        late += movement_magnitude * 0.45
        if movement_magnitude >= 8:
            warnings.append("Late market movement detected.")

    return LineMovementOutput(
        odds_movement=round(odds_move, 3) if odds_move is not None else None,
        point_movement=round(point_move, 3) if point_move is not None else None,
        movement_velocity_score=round(clamp(velocity), 2),
        directional_strength_score=round(clamp(directional), 2),
        late_move_score=round(clamp(late), 2),
        warnings=warnings,
    )
