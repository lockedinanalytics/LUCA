from __future__ import annotations

from luca.intelligence.market.v2.engine import calculate_smi_v2
from luca.intelligence.market.v2.models import SmartMoneyV2Input, SmartMoneyV2Output


def calculate_mlb_smi_v2(row: SmartMoneyV2Input) -> SmartMoneyV2Output:
    return calculate_smi_v2(row)
