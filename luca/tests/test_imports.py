from luca.objectives.engines import moneyline_edge


def test_moneyline_edge():
    result = moneyline_edge(0.58, -110)
    assert "edge" in result
