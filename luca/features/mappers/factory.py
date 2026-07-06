from __future__ import annotations

from luca.core.models import Sport
from luca.features.mappers.base import FeatureMapper
from luca.features.mappers.default import DefaultFeatureMapper
from luca.features.mappers.mlb import MlbFeatureMapper


def get_feature_mapper(sport: Sport) -> FeatureMapper:
    if sport == Sport.MLB:
        return MlbFeatureMapper()
    return DefaultFeatureMapper()
