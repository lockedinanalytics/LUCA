from __future__ import annotations

from luca.providers.mlb.features.models import MlbBoxscoreFeatures, MlbLineupSnapshot


def extract_mlb_lineup_snapshot(game_id: str, boxscore: dict, metadata: dict | None = None) -> MlbLineupSnapshot:
    metadata = metadata or {}
    return MlbLineupSnapshot(
        game_id=game_id,
        home_lineup=_extract_batters(boxscore, "home"),
        away_lineup=_extract_batters(boxscore, "away"),
        home_probable_pitcher=metadata.get("home_probable_pitcher"),
        away_probable_pitcher=metadata.get("away_probable_pitcher"),
    )


def extract_boxscore_features(game_id: str, boxscore: dict) -> MlbBoxscoreFeatures:
    warnings = []
    home_lineup = _extract_batters(boxscore, "home")
    away_lineup = _extract_batters(boxscore, "away")
    home_pitchers = _extract_pitchers(boxscore, "home")
    away_pitchers = _extract_pitchers(boxscore, "away")

    if not home_lineup:
        warnings.append("Home lineup unavailable.")
    if not away_lineup:
        warnings.append("Away lineup unavailable.")

    return MlbBoxscoreFeatures(
        game_id=game_id,
        home_lineup_count=len(home_lineup),
        away_lineup_count=len(away_lineup),
        home_pitcher_count=len(home_pitchers),
        away_pitcher_count=len(away_pitchers),
        extraction_warnings=warnings,
    )


def _extract_batters(boxscore: dict, side: str) -> list[str]:
    team = boxscore.get("teams", {}).get(side, {})
    batters = team.get("batters", []) or []
    players = team.get("players", {}) or {}
    names = []
    for player_id in batters:
        player = players.get(f"ID{player_id}", {})
        name = player.get("person", {}).get("fullName")
        if name:
            names.append(name)
    return names


def _extract_pitchers(boxscore: dict, side: str) -> list[str]:
    team = boxscore.get("teams", {}).get(side, {})
    pitchers = team.get("pitchers", []) or []
    players = team.get("players", {}) or {}
    names = []
    for player_id in pitchers:
        player = players.get(f"ID{player_id}", {})
        name = player.get("person", {}).get("fullName")
        if name:
            names.append(name)
    return names
