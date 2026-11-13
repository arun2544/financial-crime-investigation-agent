import pandas as pd

REQUIRED_COLUMNS = {"txn_id", "account_id", "counterparty", "amount", "direction", "timestamp", "channel"}

def detect_structuring(transactions: pd.DataFrame, threshold: float = 50000,
                       rolling_window_hours: int = 72,
                       min_transaction_count: int = 3) -> list[dict]:
    """Return evidence groups for repeated below-threshold credits.

    This is an educational rule only. It does not conclude that activity is criminal.
    Each result is a contiguous sequence beginning at a transaction in the time-sorted
    account history; overlapping groups are deduplicated by transaction IDs.
    """
    missing = REQUIRED_COLUMNS - set(transactions.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    if threshold <= 0 or rolling_window_hours <= 0 or min_transaction_count < 2:
        raise ValueError("threshold/window must be positive and min_transaction_count >= 2")

    df = transactions.copy()
    df["amount"] = pd.to_numeric(df["amount"], errors="raise")
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="raise")
    df["direction"] = df["direction"].astype(str).str.lower()
    df = df[(df["direction"] == "credit") & (df["amount"] < threshold)]
    evidence = []

    for account_id, group in df.sort_values("timestamp").groupby("account_id"):
        rows = group.to_dict("records")
        for start_idx in range(len(rows)):
            window = []
            start_time = rows[start_idx]["timestamp"]
            for row in rows[start_idx:]:
                if (row["timestamp"] - start_time).total_seconds() > rolling_window_hours * 3600:
                    break
                window.append(row)
                total = sum(float(item["amount"]) for item in window)
                if len(window) >= min_transaction_count and total > threshold:
                    evidence.append({
                        "account_id": str(account_id),
                        "transaction_ids": [str(item["txn_id"]) for item in window],
                        "counterparties": [str(item["counterparty"]) for item in window],
                        "channels": [str(item["channel"]) for item in window],
                        "transaction_count": len(window),
                        "total_amount": round(total, 2),
                        "window_start": start_time.isoformat(),
                        "window_end": row["timestamp"].isoformat(),
                        "rule": "multiple_below_threshold_credits_within_rolling_window"
                    })
                    break

    unique = {}
    for item in evidence:
        unique[(item["account_id"], tuple(item["transaction_ids"]))] = item
    return list(unique.values())
