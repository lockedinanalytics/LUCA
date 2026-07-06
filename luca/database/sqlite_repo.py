from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Iterable, List

from luca.database.base import LedgerRepository
from luca.ledger.models import LedgerDecision


CREATE_LEDGER_SQL = """
CREATE TABLE IF NOT EXISTS ledger_decisions (
    decision_id TEXT PRIMARY KEY,
    game_id TEXT NOT NULL,
    date TEXT NOT NULL,
    sport TEXT NOT NULL,
    league TEXT NOT NULL,
    category TEXT NOT NULL,
    market TEXT NOT NULL,
    selection TEXT NOT NULL,
    odds REAL,
    units REAL NOT NULL,
    confidence REAL NOT NULL,
    luca_score REAL,
    expected_value REAL,
    result TEXT,
    units_won_lost REAL,
    final_score TEXT,
    closing_odds REAL,
    clv REAL,
    module_snapshot TEXT NOT NULL,
    governance_snapshot TEXT NOT NULL,
    audit_status TEXT NOT NULL
);
"""


class SqliteLedgerRepository(LedgerRepository):
    def __init__(self, path: str = "luca.sqlite3"):
        self.path = Path(path)
        self._init_db()

    def _connect(self):
        return sqlite3.connect(self.path)

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(CREATE_LEDGER_SQL)
            conn.commit()

    def add_decision(self, decision: LedgerDecision) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO ledger_decisions (
                    decision_id, game_id, date, sport, league, category, market, selection,
                    odds, units, confidence, luca_score, expected_value, result,
                    units_won_lost, final_score, closing_odds, clv,
                    module_snapshot, governance_snapshot, audit_status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    decision.decision_id,
                    decision.game_id,
                    decision.date,
                    decision.sport,
                    decision.league,
                    decision.category,
                    decision.market,
                    decision.selection,
                    decision.odds,
                    decision.units,
                    decision.confidence,
                    decision.luca_score,
                    decision.expected_value,
                    decision.result,
                    decision.units_won_lost,
                    decision.final_score,
                    decision.closing_odds,
                    decision.clv,
                    json.dumps(decision.module_snapshot),
                    json.dumps(decision.governance_snapshot),
                    decision.audit_status,
                ),
            )
            conn.commit()

    def add_many(self, decisions: Iterable[LedgerDecision]) -> None:
        for decision in decisions:
            self.add_decision(decision)

    def list_decisions(self) -> List[LedgerDecision]:
        with self._connect() as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute("SELECT * FROM ledger_decisions ORDER BY date, decision_id").fetchall()

        output: list[LedgerDecision] = []
        for row in rows:
            data = dict(row)
            data["module_snapshot"] = json.loads(data["module_snapshot"] or "{}")
            data["governance_snapshot"] = json.loads(data["governance_snapshot"] or "{}")
            output.append(LedgerDecision(**data))
        return output
