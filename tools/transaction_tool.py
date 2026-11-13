from database.db import get_connection

def get_account_transactions(account_id: str) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM transactions WHERE account_id = ? ORDER BY timestamp",
            (account_id,)
        ).fetchall()
    return [dict(row) for row in rows]
