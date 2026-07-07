from __future__ import annotations

from datetime import date
from typing import Any

from luca.intelligence.mlb.starting_pitcher import StartingPitcherInput
from luca.providers.mlb.player_stats import MlbPlayerStatsProvider


class MlbPitcherAdapter:
    """
    Converts MLB Stats API pitcher data into StartingPitcherInput for LUCA.
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
            fip=self._estimate_fip(stat),
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

    def _estimate_fip(self, stat: dict[str, Any]) -> float | None:
        innings = self._to_float(stat.get("inningsPitched"))
        home_runs = self._to_float(stat.get("homeRuns"))
        walks = self._to_float(stat.get("baseOnBalls"))
        hit_by_pitch = self._to_float(stat.get("hitBatsmen"))
        strikeouts = self._to_float(stat.get("strikeOuts"))

        if innings in (None, 0):
            return None

        return round(
            (
                (13 * (home_runs or 0))
                + (3 * ((walks or 0) + (hit_by_pitch or 0)))
                - (2 * (strikeouts or 0))
            )
            / innings
            + 3.1,
            2,
        )

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
