from __future__ import annotations

from luca.core.models import Sport
from luca.features.mappers.base import FeatureMapper
from luca.features.mappers.default import DefaultFeatureMapper
from luca.features.mappers.mlb import MlbFeatureMapper
from luca.features.mappers.nfl.mapper import NflFeatureMapper
from luca.features.mappers.ncaaf.mapper import NcaafFeatureMapper
from luca.features.mappers.soccer.mapper import SoccerFeatureMapper


def get_feature_mapper(sport: Sport) -> FeatureMapper:
    if sport == Sport.MLB:
        return MlbFeatureMapper()
    if sport == Sport.NFL:
        return NflFeatureMapper()
    if sport == Sport.NCAAF:
        return NcaafFeatureMapper()
    if sport == Sport.SOCCER:
        return SoccerFeatureMapper()
    return DefaultFeatureMapper()
