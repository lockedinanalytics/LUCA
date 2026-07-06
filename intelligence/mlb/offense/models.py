from __future__ import annotations

from pydantic import BaseModel, Field


class HitterInput(BaseModel):
    name: str
    lineup_spot: int
    handedness: str = "R"
    xwoba_score: float = 50.0
    xslg_score: float = 50.0
    hard_hit_score: float = 50.0
    barrel_score: float = 50.0
    contact_score: float = 50.0
    chase_discipline_score: float = 50.0
    strikeout_avoidance_score: float = 50.0
    walk_score: float = 50.0
    platoon_score: float = 50.0
    pitch_type_fit_score: float = 50.0
    baserunning_score: float = 50.0
    recent_form_score: float = 50.0
    injury_penalty: float = 0.0


class HitterQualityOutput(BaseModel):
    name: str
    lineup_spot: int
    on_base_score: float
    damage_score: float
    discipline_score: float
    matchup_score: float
    final_hitter_score: float
    warnings: list[str] = Field(default_factory=list)


class LineupChainInput(BaseModel):
    hitters: list[HitterInput] = Field(default_factory=list)
    bench_score: float = 50.0
    pinch_hit_score: float = 50.0


class LineupChainOutput(BaseModel):
    top_four_score: float
    bottom_five_score: float
    on_base_chain_score: float
    power_cascade_score: float
    strikeout_cluster_risk: float
    lineup_depth_score: float
    bench_adjustment_score: float
    final_chain_score: float
    warnings: list[str] = Field(default_factory=list)
    hitter_scores: dict[str, float] = Field(default_factory=dict)


class PlatoonInput(BaseModel):
    projected_lhp_plate_appearances: float = 0.0
    projected_rhp_plate_appearances: float = 0.0
    lineup_platoon_score: float = 50.0
    switch_hitter_flex_score: float = 50.0
    opposing_pitcher_hand: str | None = None
    opposing_bullpen_hand_balance_score: float = 50.0


class PlatoonOutput(BaseModel):
    starter_platoon_score: float
    bullpen_platoon_score: float
    flexibility_score: float
    final_platoon_score: float
    warnings: list[str] = Field(default_factory=list)


class RunCreationV2Input(BaseModel):
    hitters: list[HitterInput] = Field(default_factory=list)
    bench_score: float = 50.0
    pinch_hit_score: float = 50.0
    platoon: PlatoonInput = Field(default_factory=PlatoonInput)
    park_factor: float = 1.0
    weather_total_adjustment: float = 0.0
    opposing_starting_pitcher_score: float = 50.0
    opposing_bullpen_score: float = 50.0
    expected_plate_appearances: float = 38.0


class RunCreationV2Output(BaseModel):
    lineup_chain_score: float
    platoon_score: float
    starter_matchup_score: float
    bullpen_matchup_score: float
    run_environment_score: float
    projected_runs: float
    explosive_inning_probability: float
    final_rcp_score: float
    confidence: float
    warnings: list[str] = Field(default_factory=list)
    explainability: dict[str, float] = Field(default_factory=dict)
