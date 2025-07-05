from __future__ import annotations

import sqlite3
from pathlib import Path

DB_PATH = Path("data/localpulse.db")

SCHEMA = Path(__file__).with_name("schema.sql")


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH, isolation_level=None)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn


def init_db() -> None:
    conn = get_connection()
    sql = SCHEMA.read_text()
    conn.executescript(sql)

