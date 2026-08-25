from __future__ import annotations

import pytest

from luca.providers.mlb.adapters.pitcher_adapters import MlbPitcherAdapter


class _Provider:
    def get_pitcher_stats(self, pitcher_id, *, season):
        return {
            "people": [
                {
                    "stats": [
                        {
                            "splits": [
                                {
                                    "stat": {
                                        "inningsPitched": "100.0",
                                        "strikeOuts": 120,
                                        "baseOnBalls": 30,
                                        "battersFaced": 400,
                                        "homeRuns": 10,
                                        "hitBatsmen": 2,
                                        "era": "3.25",
                                    }
                                }
                            ]
                        }
                    ]
                }
            ]
        }


def test_pitcher_adapter_maps_rates_and_estimates_missing_fip():
    adapter = MlbPitcherAdapter()
    adapter.player_stats_provider = _Provider()

    result = adapter.build(123)

    assert result.xera == 3.25
    assert result.strikeout_rate == 30.0
    assert result.walk_rate == 7.5
    assert result.fip == pytest.approx(2.96)
