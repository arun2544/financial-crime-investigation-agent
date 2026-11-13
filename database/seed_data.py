import json
from pathlib import Path
import pandas as pd
from database.db import get_connection, initialize_database

def main():
    cfg = json.loads(Path("config/config.json").read_text(encoding="utf-8"))
    initialize_database()
    tables = [
        ("transactions", cfg["transactions_csv"]),
        ("account_profiles", cfg["profiles_csv"]),
        ("previous_alerts", cfg["alerts_csv"]),
    ]
    with get_connection() as conn:
        for table, csv_path in tables:
            df = pd.read_csv(csv_path)
            df.to_sql(table, conn, if_exists="replace", index=False)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_txn_account_time ON transactions(account_id, timestamp)")
    print("SQLite database seeded from CSV files.")

if __name__ == "__main__":
    main()
