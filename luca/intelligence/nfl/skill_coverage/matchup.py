from __future__ import annotations

from luca.intelligence.nfl.skill_coverage.coverage import score_coverage_unit
from luca.intelligence.nfl.skill_coverage.models import SkillCoverageMatchupInput, SkillCoverageMatchupOutput
from luca.intelligence.nfl.skill_coverage.receivers import score_receiver_unit
from luca.intelligence.nfl.skill_coverage.running_back import score_running_back
from luca.intelligence.nfl.skill_coverage.tight_end import score_tight_end


def calculate_skill_coverage_matchup(row: SkillCoverageMatchupInput) -> SkillCoverageMatchupOutput:
    receivers = score_receiver_unit(row.receivers)
    tight_end = score_tight_end(row.tight_end)
    running_back = score_running_back(row.running_back)
    coverage = score_coverage_unit(row.coverage)

    warnings = []
    warnings.extend(receivers.warnings)
    warnings.extend(tight_end.warnings)
    warnings.extend(running_back.warnings)
    warnings.extend(coverage.warnings)

    wr_cb = (
        receivers.final_receiver_score * 0.42
        + row.quarterback_accuracy_score * 0.16
        + row.pass_protection_score * 0.12
        + row.offensive_scheme_score * 0.12
        + (100 - coverage.final_coverage_score) * 0.18
    )

    te_matchup = (
        tight_end.final_te_score * 0.46
        + (100 - (row.coverage.linebacker_coverage_score if row.coverage.linebacker_coverage_score is not None else 50.0)) * 0.20
        + (100 - (row.coverage.safety_help_score if row.coverage.safety_help_score is not None else 50.0)) * 0.16
        + row.offensive_scheme_score * 0.18
    )

    rb_matchup = (
        running_back.final_rb_score * 0.42
        + running_back.receiving_value_score * 0.18
        + (100 - (row.coverage.linebacker_coverage_score if row.coverage.linebacker_coverage_score is not None else 50.0)) * 0.18
        + row.pass_protection_score * 0.12
        + row.offensive_scheme_score * 0.10
    )

    explosive_pass = (
        receivers.explosive_skill_score * 0.36
        + row.quarterback_accuracy_score * 0.18
        + row.pass_protection_score * 0.16
        + (100 - coverage.explosive_prevention_score) * 0.22
        + row.offensive_scheme_score * 0.08
    )

    possession_chain = (
        receivers.possession_skill_score * 0.30
        + tight_end.receiving_matchup_score * 0.18
        + running_back.receiving_value_score * 0.14
        + row.quarterback_accuracy_score * 0.18
        + row.offensive_scheme_score * 0.12
        + (100 - coverage.matchup_flexibility_score) * 0.08
    )

    red_zone = (
        tight_end.red_zone_score * 0.24
        + running_back.goal_line_value_score * 0.18
        + receivers.possession_skill_score * 0.18
        + row.quarterback_accuracy_score * 0.16
        + row.offensive_scheme_score * 0.12
        + (100 - coverage.coverage_quality_score) * 0.12
    )

    final = (
        wr_cb * 0.24
        + te_matchup * 0.12
        + rb_matchup * 0.10
        + explosive_pass * 0.20
        + possession_chain * 0.18
        + red_zone * 0.16
    )

    populated = 0
    total = 0
    for section in [row.receivers, row.tight_end, row.running_back, row.coverage, row]:
        data = section.model_dump()
        total += len(data)
        populated += sum(v is not None for v in data.values())
    confidence = 45 + min(45, populated / max(1, total) * 45)
    if warnings:
        confidence -= min(10, len(warnings))

    explainability = {
        "receivers": receivers.final_receiver_score,
        "tight_end": tight_end.final_te_score,
        "running_back": running_back.final_rb_score,
        "coverage": coverage.final_coverage_score,
        "wr_cb": round(wr_cb, 2),
        "te": round(te_matchup, 2),
        "rb": round(rb_matchup, 2),
        "explosive_pass": round(explosive_pass, 2),
        "possession_chain": round(possession_chain, 2),
        "red_zone": round(red_zone, 2),
    }

    return SkillCoverageMatchupOutput(
        receiver_score=receivers.final_receiver_score,
        tight_end_score=tight_end.final_te_score,
        running_back_score=running_back.final_rb_score,
        coverage_score=coverage.final_coverage_score,
        wr_cb_matchup_score=round(max(0, min(100, wr_cb)), 2),
        te_matchup_score=round(max(0, min(100, te_matchup)), 2),
        rb_matchup_score=round(max(0, min(100, rb_matchup)), 2),
        explosive_pass_projection=round(max(0, min(100, explosive_pass)), 2),
        possession_chain_score=round(max(0, min(100, possession_chain)), 2),
        red_zone_skill_score=round(max(0, min(100, red_zone)), 2),
        final_skill_coverage_score=round(max(0, min(100, final)), 2),
        confidence=round(max(0, min(100, confidence)), 2),
        warnings=warnings,
        explainability=explainability,
    )
