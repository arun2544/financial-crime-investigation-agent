import json
import sqlite3
from pathlib import Path

CONFIG = json.loads(Path("config/config.json").read_text(encoding="utf-8"))
DB_PATH = Path(CONFIG["database_path"])

def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    with get_connection() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS transactions (
            txn_id TEXT PRIMARY KEY,
            account_id TEXT NOT NULL,
            counterparty TEXT,
            amount REAL NOT NULL,
            direction TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            channel TEXT
        );
        CREATE TABLE IF NOT EXISTS account_profiles (
            account_id TEXT PRIMARY KEY,
            account_type TEXT,
            account_open_date TEXT,
            occupation TEXT,
            expected_monthly_volume REAL,
            notes TEXT
        );
        CREATE TABLE IF NOT EXISTS previous_alerts (
            alert_id TEXT PRIMARY KEY,
            account_id TEXT NOT NULL,
            alert_type TEXT,
            created_at TEXT,
            status TEXT,
            notes TEXT
        );
        CREATE INDEX IF NOT EXISTS idx_txn_account_time
        ON transactions(account_id, timestamp);
        """)
