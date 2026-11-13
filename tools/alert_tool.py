from database.db import get_connection

def get_previous_alerts(account_id: str) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM previous_alerts WHERE account_id = ? ORDER BY created_at DESC",
            (account_id,)
        ).fetchall()
    return [dict(row) for row in rows]
