from database.db import get_connection

def get_account_profile(account_id: str) -> dict | None:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM account_profiles WHERE account_id = ?", (account_id,)
        ).fetchone()
    return dict(row) if row else None
