from __future__ import annotations

from datetime import date
from typing import Any

from luca.intelligence.mlb.starting_pitcher import (
    StartingPitcherInput,
)
from luca.providers.mlb.player_stats import MlbPlayerStatsProvider


class MlbPitcherAdapter:
    """
    Converts MLB Stats API pitcher data into
    StartingPitcherInput for LUCA.
    """

    def __init__(self):
        self.provider = MlbPlayerStatsProvider()

    def build_for_home_pitcher(self, game: Any) -> StartingPitcherInput:
        metadata = getattr(game, "metadata", {}) or {}
        pitcher_id = metadata.get("home_probable_pitcher_id")
        return self.build(pitcher_id)

    def build_for_away_pitcher(self, game: Any) -> StartingPitcherInput:
        metadata = getattr(game, "metadata", {}) or {}
        pitcher_id = metadata.get("away_probable_pitcher_id")
        return self.build(pitcher_id)

    def build(self, pitcher_id: int | str | None) -> StartingPitcherInput:
        if not pitcher_id:
            return StartingPitcherInput()

        try:
            payload = self.provider.get_pitcher_stats(
                pitcher_id,
                season=date.today().year,
            )
        except Exception:
            return StartingPitcherInput()

        stat = self._extract_pitching_stat(payload)

        if not stat:
            return StartingPitcherInput()

        strikeouts = self._to_float(stat.get("strikeOuts"))
        walks = self._to_float(stat.get("baseOnBalls"))
        batters = self._to_float(stat.get("battersFaced"))

        return StartingPitcherInput(
            xera=self._to_float(stat.get("era")),
            fip=self._to_float(stat.get("fip")),
            strikeout_rate=self._percent(strikeouts, batters),
            walk_rate=self._percent(walks, batters),
            hard_hit_rate=None,
            barrel_rate=None,
            recent_pitch_count=None,
            days_rest=None,
        )

    def _extract_pitching_stat(self, payload: dict[str, Any]) -> dict[str, Any]:
        people = payload.get("people", [])

        if not people:
            return {}

        stats = people[0].get("stats", [])

        for stat_group in stats:
            splits = stat_group.get("splits", [])

            if not splits:
                continue

            stat = splits[0].get("stat")

            if stat:
                return stat

        return {}

    @staticmethod
    def _to_float(value: Any) -> float | None:
        if value is None:
            return None

        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _percent(
        numerator: float | None,
        denominator: float | None,
    ) -> float | None:
        if numerator is None:
            return None

        if denominator in (None, 0):
            return None

        return round((numerator / denominator) * 100.0, 2)
