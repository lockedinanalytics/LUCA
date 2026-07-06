from __future__ import annotations

from luca.intelligence.mlb.pitching.arsenal import score_pitch_arsenal
from luca.intelligence.mlb.pitching.command import score_command
from luca.intelligence.mlb.pitching.contact import score_contact_management
from luca.intelligence.mlb.pitching.fatigue import score_pitcher_fatigue
from luca.intelligence.mlb.pitching.matchup import score_pitcher_matchup
from luca.intelligence.mlb.pitching.models import StartingPitcherIntelligenceInput, StartingPitcherIntelligenceOutput


def calculate_starting_pitcher_intelligence(row: StartingPitcherIntelligenceInput) -> StartingPitcherIntelligenceOutput:
    arsenal = score_pitch_arsenal(row.arsenal)
    command = score_command(row.command)
    contact = score_contact_management(row.contact)
    fatigue = score_pitcher_fatigue(row.fatigue)
    matchup = score_pitcher_matchup(row.matchup)

    warnings = []
    for block in [arsenal, command, contact, fatigue, matchup]:
        warnings.extend(block.notes)

    final = (
        arsenal.final_arsenal_score * 0.24
        + command.final_command_score * 0.20
        + contact.final_contact_score * 0.22
        + fatigue.final_fatigue_score * 0.16
        + matchup.final_matchup_score * 0.18
    )

    populated = 0
    total = 0
    for section in [row.arsenal, row.command, row.contact, row.fatigue, row.matchup]:
        data = section.model_dump()
        total += len(data)
        populated += sum(value is not None for value in data.values())
    confidence = 50 + (populated / total) * 45 if total else 50

    explainability = {
        "arsenal": arsenal.final_arsenal_score,
        "command": command.final_command_score,
        "contact": contact.final_contact_score,
        "fatigue": fatigue.final_fatigue_score,
        "matchup": matchup.final_matchup_score,
    }

    return StartingPitcherIntelligenceOutput(
        arsenal_score=arsenal.final_arsenal_score,
        command_score=command.final_command_score,
        contact_score=contact.final_contact_score,
        fatigue_score=fatigue.final_fatigue_score,
        matchup_score=matchup.final_matchup_score,
        final_sp_score=round(max(0, min(100, final)), 2),
        confidence=round(max(0, min(100, confidence)), 2),
        warnings=warnings,
        explainability=explainability,
    )
