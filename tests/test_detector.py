import pandas as pd
import pytest
from detector.structuring import detect_structuring

COLS = ["txn_id", "account_id", "counterparty", "amount", "direction", "timestamp", "channel"]

def test_detects_multiple_credits_over_threshold():
    df = pd.DataFrame([
        ["T1","A1","P1",18000,"credit","2026-01-01T08:00:00","UPI"],
        ["T2","A1","P2",17000,"credit","2026-01-02T08:00:00","IMPS"],
        ["T3","A1","P3",19000,"credit","2026-01-03T08:00:00","NEFT"],
    ], columns=COLS)
    result = detect_structuring(df, threshold=50000, rolling_window_hours=72, min_transaction_count=3)
    assert len(result) == 1
    assert result[0]["total_amount"] == 54000
    assert result[0]["transaction_ids"] == ["T1", "T2", "T3"]

def test_ignores_debits():
    df = pd.DataFrame([
        ["T1","A1","P1",18000,"debit","2026-01-01T08:00:00","UPI"],
        ["T2","A1","P2",17000,"debit","2026-01-02T08:00:00","IMPS"],
        ["T3","A1","P3",19000,"debit","2026-01-03T08:00:00","NEFT"],
    ], columns=COLS)
    assert detect_structuring(df) == []

def test_single_credit_above_threshold_is_not_structuring_rule():
    df = pd.DataFrame([
        ["T1","A1","P1",118253.33,"credit","2026-01-03T15:02:00","IMPS"],
    ], columns=COLS)
    assert detect_structuring(df) == []

def test_missing_column_raises():
    with pytest.raises(ValueError):
        detect_structuring(pd.DataFrame({"txn_id": ["T1"]}))
