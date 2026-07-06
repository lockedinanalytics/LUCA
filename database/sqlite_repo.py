import json, sqlite3
from pathlib import Path
from luca.database.base import LedgerRepository
from luca.ledger.models import LedgerDecision

SQL = '''CREATE TABLE IF NOT EXISTS ledger_decisions (
decision_id TEXT PRIMARY KEY, game_id TEXT, date TEXT, sport TEXT, league TEXT, category TEXT, market TEXT, selection TEXT,
odds REAL, units REAL, confidence REAL, luca_score REAL, expected_value REAL, result TEXT, units_won_lost REAL,
final_score TEXT, closing_odds REAL, clv REAL, module_snapshot TEXT, governance_snapshot TEXT, audit_status TEXT);'''

class SqliteLedgerRepository(LedgerRepository):
    def __init__(self, path: str="luca.sqlite3"):
        self.path=Path(path)
        with sqlite3.connect(self.path) as c: c.execute(SQL)
    def add_decision(self, d: LedgerDecision) -> None:
        with sqlite3.connect(self.path) as c:
            c.execute('INSERT OR REPLACE INTO ledger_decisions VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
            (d.decision_id,d.game_id,d.date,d.sport,d.league,d.category,d.market,d.selection,d.odds,d.units,d.confidence,d.luca_score,d.expected_value,d.result,d.units_won_lost,d.final_score,d.closing_odds,d.clv,json.dumps(d.module_snapshot),json.dumps(d.governance_snapshot),d.audit_status))
    def list_decisions(self) -> list[LedgerDecision]:
        with sqlite3.connect(self.path) as c:
            c.row_factory=sqlite3.Row
            rows=c.execute('SELECT * FROM ledger_decisions ORDER BY date, decision_id').fetchall()
        out=[]
        for r in rows:
            data=dict(r); data["module_snapshot"]=json.loads(data["module_snapshot"] or "{}"); data["governance_snapshot"]=json.loads(data["governance_snapshot"] or "{}")
            out.append(LedgerDecision(**data))
        return out
