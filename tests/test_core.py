from luca.analytics.engines import universal_power_rating, luca_composite_intelligence
from luca.objectives.engines import moneyline_edge
from luca.features.registry import list_features

def test_universal_power_rating():
    assert 0 <= universal_power_rating({"offense": 80, "defense": 70, "availability": 90}) <= 100

def test_luca_composite():
    assert 0 <= luca_composite_intelligence({"upr_edge": 80, "cae": 75, "edge": 70}) <= 100

def test_moneyline_edge():
    assert "edge" in moneyline_edge(0.58, -110)

def test_features_loaded():
    assert len(list_features()) > 0
