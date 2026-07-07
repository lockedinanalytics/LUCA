from __future__ import annotations

from datetime import date
from typing import Any

from luca.intelligence.mlb.starting_pitcher import StartingPitcherInput
from luca.providers.mlb.player_stats import MlbPlayerStatsProvider


class MlbPitcherAdapter:
    """
    Converts MLB player/pitcher provider data into StartingPitcherInput.
    """

    def __init__(self):
        self.player_stats_provider = MlbPlayerStatsProvider()

    def build_for_home_pitcher(self, game: Any) -> StartingPitcherInput:
        metadata = getattr(game, "metadata", {}) or {}
        pitcher_id = metadata.get("home_probable_pitcher_id")
        return self.build(pitcher_id)

    def build_for_away_pitcher(self, game: Any) -> StartingPitcherInput:
        metadata = getattr(game, "metadata", {}) or {}
        pitcher_id = metadata.get("away_probable_pitcher_id")
        return self.build(pitcher_id)

    def build(self, pitcher_id: str | int | None) -> StartingPitcherInput:
        if not pitcher_id:
            return StartingPitcherInput()

        try:
            payload = self.player_stats_provider.get_pitcher_stats(
                pitcher_id,
                season=date.today().year,
            )
        except Exception:
            return StartingPitcherInput()

        stat = self._extract_pitching_stat(payload)
        if not stat:
            return StartingPitcherInput()

        innings = self._to_float(stat.get("inningsPitched"))
        strikeouts = self._to_float(stat.get("strikeOuts"))
        walks = self._to_float(stat.get("baseOnBalls"))
        batters_faced = self._to_float(stat.get("battersFaced"))

        strikeout_rate = self._rate(strikeouts, batters_faced)
        walk_rate = self._rate(walks, batters_faced)

        fip = self._to_float(stat.get("fip"))
        era = self._to_float(stat.get("era"))

        return StartingPitcherInput(
            xera=era,
            fip=fip,
            strikeout_rate=strikeout_rate,
            walk_rate=walk_rate,
            hard_hit_rate=None,
            barrel_rate=None,
            recent_pitch_count=None,
            days_rest=None,
        )

    def _extract_pitching_stat(self, payload: dict[str, Any]) -> dict[str, Any]:
        people = payload.get("people", [])
        if not people:
            return {}

        person = people[0]
        stats = person.get("stats", [])

        for stat_group in stats:
            splits = stat_group.get("splits", [])
            if not splits:
                continue
            stat = splits[0].get("stat", {})
            if stat:
                return stat

        return {}

    def _rate(self, numerator: float | None, denominator: float | None) -> float | None:
        if numerator is None or denominator in (None, 0):
            return None
        return round((numerator / denominator) * 100, 2)

    def _to_float(self, value: Any) -> float | None:
        if value is None:
            return None

        try:
            return float(value)
        except (TypeError, ValueError):
            return None
