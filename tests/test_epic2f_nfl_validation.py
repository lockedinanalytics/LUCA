from luca.governance.promotion.nfl import build_nfl_promotion_record, evaluate_nfl_promotion_gate
from luca.validation.nfl.engine import build_nfl_validation_summary
from luca.validation.nfl.models import NflPromotionGateInput, NflReplayInput
from luca.validation.replay.models import HistoricalDecision


def sample_decisions():
    rows = []
    markets = ["moneyline", "spread", "total"]
    for i in range(1, 121):
        market = markets[i % 3]
        confidence = 56 + (i % 9) * 4
        win = i % 4 != 0
        rows.append(HistoricalDecision(
            decision_id=f"nfl-{i}",
            date="2026-09-01",
            sport="nfl",
            league="NFL",
            game_id=f"game-{i}",
            market=market,
            category="cabinet",
            selection="Home",
            odds=-110,
            units=1.0,
            confidence=confidence,
            projected_probability=confidence / 100,
            result="win" if win else "loss",
            units_won_lost=0.91 if win else -1.0,
            closing_odds=-118 if win else -104,
            module_snapshot={"qb_edge": 55 + (i % 10), "market_edge": 51 + (i % 9)},
        ))
    return rows


def test_nfl_validation_summary():
    summary = build_nfl_validation_summary(NflReplayInput(replay_id="x", model_version="test", decisions=sample_decisions()))
    assert summary.graded_decisions == 120
    assert len(summary.market_slices) == 3


def test_nfl_promotion_gate_record():
    summary = build_nfl_validation_summary(NflReplayInput(replay_id="x", model_version="test", decisions=sample_decisions()))
    gate = evaluate_nfl_promotion_gate(NflPromotionGateInput(validation=summary))
    record = build_nfl_promotion_record("p1", "old", "new", gate)
    assert record.sport == "nfl"
    assert record.to_version == "new"
