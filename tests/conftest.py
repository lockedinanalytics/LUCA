from __future__ import annotations

import pytest

from luca.config.settings import get_settings


@pytest.fixture(autouse=True)
def isolate_cached_settings():
    """Every test observes its own environment-variable configuration."""
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()
