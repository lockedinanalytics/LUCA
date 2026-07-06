from __future__ import annotations

from luca.intelligence.mlb.pitching.models import MatchupInput, MatchupOutput


def score_pitcher_matchup(row: MatchupInput) -> MatchupOutput:
    notes: list[str] = []

    pitch_fit = 50.0
    if row.opponent_fastball_run_value is not None:
        pitch_fit += -row.opponent_fastball_run_value * 1.5
    if row.opponent_breaking_ball_run_value is not None:
        pitch_fit += -row.opponent_breaking_ball_run_value * 1.8
    if row.opponent_offspeed_run_value is not None:
        pitch_fit += -row.opponent_offspeed_run_value * 1.4

    bat_missing = 50.0
    if row.opponent_whiff_rate is not None:
        bat_missing += (row.opponent_whiff_rate - 23.0) * 0.9
    if row.opponent_chase_rate is not None:
        bat_missing += (row.opponent_chase_rate - 28.0) * 0.6

    platoon = 50.0
    if row.opponent_platoon_advantage_score is not None:
        platoon += (50.0 - row.opponent_platoon_advantage_score) * 0.55
    if row.projected_lineup_hand_balance_score is not None:
        platoon += (row.projected_lineup_hand_balance_score - 50.0) * 0.20

    if pitch_fit < 45:
        notes.append("Pitch-type matchup leans toward opposing lineup.")
    if platoon < 45:
        notes.append("Platoon configuration is unfavorable.")

    final = pitch_fit * 0.40 + bat_missing * 0.30 + platoon * 0.30

    return MatchupOutput(
        pitch_type_fit_score=round(max(0, min(100, pitch_fit)), 2),
        bat_missing_fit_score=round(max(0, min(100, bat_missing)), 2),
        platoon_fit_score=round(max(0, min(100, platoon)), 2),
        final_matchup_score=round(max(0, min(100, final)), 2),
        notes=notes,
    )
