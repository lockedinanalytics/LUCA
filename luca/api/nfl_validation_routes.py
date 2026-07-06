from __future__ import annotations

from fastapi import APIRouter

from luca.governance.promotion.nfl import build_nfl_promotion_record, evaluate_nfl_promotion_gate
from luca.validation.nfl.engine import build_nfl_validation_summary
from luca.validation.nfl.models import NflPromotionGateInput, NflReplayInput
from luca.validation.replay.models import HistoricalDecision

router = APIRouter(prefix="/validation/nfl", tags=["nfl-validation"])


def sample_nfl_decisions() -> list[HistoricalDecision]:
    rows = []
    markets = ["moneyline", "spread", "total"]
    for i in range(1, 121):
        market = markets[i % 3]
        confidence = 56 + (i % 9) * 4
        win = i % 4 != 0
        odds = -110
        closing = -118 if win else -104
        rows.append(HistoricalDecision(
            decision_id=f"nfl-{i}",
            date="2026-09-01",
            sport="nfl",
            league="NFL",
            game_id=f"game-{i}",
            market=market,
            category="presidential" if i % 20 == 0 else "cabinet",
            selection="Home",
            odds=odds,
            units=1.0,
            confidence=confidence,
            projected_probability=confidence / 100,
            luca_score=confidence + 3,
            result="win" if win else "loss",
            units_won_lost=0.91 if win else -1.0,
            closing_odds=closing,
            module_snapshot={
                "qb_edge": 55 + (i % 10),
                "ol_dl_edge": 54 + (i % 8),
                "skill_coverage_edge": 53 + (i % 7),
                "context_edge": 52 + (i % 6),
                "market_edge": 51 + (i % 9),
            },
        ))
    return rows


@router.get("/summary/sample")
async def summary_sample():
    return build_nfl_validation_summary(NflReplayInput(
        replay_id="nfl-sample",
        model_version="1.0.0-epic2f",
        decisions=sample_nfl_decisions(),
    )).model_dump()


@router.get("/promotion/sample")
async def promotion_sample():
    validation = build_nfl_validation_summary(NflReplayInput(
        replay_id="nfl-sample",
        model_version="1.0.0-epic2f",
        decisions=sample_nfl_decisions(),
    ))
    gate = evaluate_nfl_promotion_gate(NflPromotionGateInput(validation=validation))
    return build_nfl_promotion_record(
        promotion_id="nfl-promo-sample",
        from_version="1.0.0-epic2e",
        to_version="1.0.0-epic2f",
        gate=gate,
    ).model_dump()
