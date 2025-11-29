import sqlite3
from typing import Iterable, Dict, Any

DB_PATH = "data/store.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS nodes (
    id TEXT PRIMARY KEY,
    label TEXT,
    meta TEXT
);
CREATE TABLE IF NOT EXISTS edges (
    source TEXT,
    target TEXT,
    weight REAL,
    kind TEXT,
    PRIMARY KEY (source, target)
);
"""

class Persistence:
    def __init__(self, path: str = DB_PATH):
        self.path = path
        self._init()

    def _init(self):
        con = sqlite3.connect(self.path)
        try:
            con.executescript(SCHEMA)
            con.commit()
        finally:
            con.close()

    def save_nodes(self, items: Iterable[Dict[str, Any]]):
        con = sqlite3.connect(self.path)
        try:
            for n in items:
                con.execute(
                    "INSERT OR REPLACE INTO nodes (id, label, meta) VALUES (?, ?, ?)",
                    (n["id"], n.get("label"), str(n.get("meta", {})))
                )
            con.commit()
        finally:
            con.close()

    def save_edges(self, items: Iterable[Dict[str, Any]]):
        con = sqlite3.connect(self.path)
        try:
            for e in items:
                con.execute(
                    "INSERT OR REPLACE INTO edges (source, target, weight, kind) VALUES (?, ?, ?, ?)",
                    (e["source"], e["target"], float(e.get("weight", 1.0)), e.get("kind", "association"))
                )
            con.commit()
        finally:
            con.close()

    def load_nodes(self):
        con = sqlite3.connect(self.path)
        try:
            cur = con.execute("SELECT id, label, meta FROM nodes")
            return [{"id": r[0], "label": r[1], "meta": {}} for r in cur.fetchall()]
        finally:
            con.close()

    def load_edges(self):
        con = sqlite3.connect(self.path)
        try:
            cur = con.execute("SELECT source, target, weight, kind FROM edges")
            return [{"source": r[0], "target": r[1], "weight": r[2], "kind": r[3]} for r in cur.fetchall()]
        finally:
            con.close()
