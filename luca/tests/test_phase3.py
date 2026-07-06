from luca.providers.aliases.resolver import TeamAliasResolver
from luca.core.models import Sport
from luca.providers.factory import get_schedule_provider
from luca.features.mappers.factory import get_feature_mapper


def test_alias_resolver():
    resolver = TeamAliasResolver()
    assert resolver.canonicalize("LAD", sport="mlb", league="MLB") == "Los Angeles Dodgers"


def test_nfl_static_provider():
    provider = get_schedule_provider("nfl_static")
    games = provider.get_games(Sport.NFL, "NFL", "2026-08-01")
    assert len(games) == 1


def test_nfl_feature_mapper():
    mapper = get_feature_mapper(Sport.NFL)
    game = get_schedule_provider("nfl_static").get_games(Sport.NFL, "NFL", "2026-08-01")[0]
    modules = mapper.build_modules(game, [])
    assert "qb_edge" in modules
