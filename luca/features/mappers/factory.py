from __future__ import annotations

from luca.core.models import Sport
from luca.features.mappers.base import FeatureMapper
from luca.features.mappers.default import DefaultFeatureMapper


def get_feature_mapper(sport: Sport) -> FeatureMapper:
    if sport == Sport.MLB:
        from luca.features.mappers.mlb import MlbFeatureMapper
        return MlbFeatureMapper()

    if sport == Sport.NFL:
        from luca.features.mappers.nfl.mapper import NflFeatureMapper
        return NflFeatureMapper()

    if sport == Sport.NCAAF:
        from luca.features.mappers.ncaaf.mapper import NcaafFeatureMapper
        return NcaafFeatureMapper()

    if sport == Sport.SOCCER:
        from luca.features.mappers.soccer.mapper import SoccerFeatureMapper
        return SoccerFeatureMapper()

    return DefaultFeatureMapper()
